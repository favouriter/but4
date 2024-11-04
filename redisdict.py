import aioredis, asyncio, json
class RedisDict(dict):
    def __init__(self, prefix, redis_conn, auto_clear=True, interval=60, **kwargs):
        super().__init__(**kwargs)
        self.prefix, self.redis_conn = prefix, redis_conn
        self.auto_clear, self.interval, self.clear_at = auto_clear, interval, self.now_at()

    def __getitem__(self, key):
        value = super().__getitem__(key) if key in self else None
        if value is not None: return value
        return asyncio.run(self.read_redis(key))

    def get(self, key, default=None):
        value = super().get(key, default)
        if value is not None: return value
        return asyncio.run(self.read_redis(key))


    def update(self, E=None, **kwargs):
        if E is not None: kwargs.update(E)
        super().update(**kwargs)
        for k,v in kwargs.items():
            asyncio.create_task(self.save2redis(k,v))

    # 修改配置，同步到redis
    def __setitem__(self, key, value, from_redis=False):
        super().__setitem__(key, value)
        if not from_redis:
            asyncio.create_task(self.save2redis(key, value))

    # 从远程获取数据
    async def read_redis(self, key):
        value = await self.redis_conn.get(self.foramt_redis_key(key))
        if value is not None:
            value = value.decode()
            super().update({key: value})
        self.do_auto_cdolear()
        return value

    # 保存到远程(redis)
    async def save2redis(self, key, value):
        redis_value = await self.redis_conn.get(self.foramt_redis_key(key))
        if redis_value is None or redis_value.decode() != value:
            await self.redis_conn.set(self.foramt_redis_key(key), value, ex=60*60)
            await self.publish(key, value)
        self.do_auto_cdolear()

    # 执行自动清理本地数据
    def do_auto_cdolear(self):
        if not self.auto_clear: return
        now_at = self.now_at()
        if now_at - self.clear_at > self.interval:
            self.clear_at = now_at
            self.clear()

    # 获取当前时间
    def now_at(self): return int(time.time())

    # 格式化redis的key
    def foramt_redis_key(self, key):
        return f'{self.prefix}_{key}'

    # 发布更新
    async def publish(self, key, value):
        msg = {key:value}
        await self.redis_conn.publish(self.prefix, json.dumps(msg))

    # 订阅更新
    async def subscribe(self):
        channel = self.redis_conn.psubscribe(self.prefix)
        async for msg in channel.iter():
            msg_dict = json.loads(msg)
            for key, value in msg_dict.items:
                if key in self:
                    self.__setitem__(key, value, from_redis=True)
                    # self.update({key: value})

