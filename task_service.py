class Service:
    def __init__(self,repo):
        self.repo=repo

    async def check_get_user(self,name):
        if not name:
            raise ValueError('Недостаточно данных!')
        return await self.repo.get_user(name)

    async def check_add_user(self,name,password):
        if not name or not password:
            raise ValueError('Недостаточно данных!')
        return await self.repo.add_user(name,password)

    async def check_add_poll(self,name,password):
        if not name or not password:
            raise ValueError('Недостаточно данных!')
        return await self.repo.add_poll(name,password)

    async def check_get_all(self,CLASS, filter):
        if not CLASS:
            raise ValueError('Недостаточно данных!')
        return await self.repo.get_all(CLASS,filter)

    async def check_get_all_types(self,id, all=True):
            if not id:
                raise ValueError('Недостаточно данных!')
            return await self.repo.get_all_types(id,all)

    async def check_get_answer(self, user_id, vote_id):
            if not id:
                raise ValueError('Недостаточно данных!')
            return await self.repo.get_answer(user_id,vote_id)