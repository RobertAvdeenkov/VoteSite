from sqlalchemy import select
from models import *
from fastapi import HTTPException
import bcrypt

class Repository:
    def __init__(self,db):
        self.db=db

    async def get_user(self,name):
        ex=select(User).filter(User.name==name)
        res=(await self.db.execute(ex)).first()
        if not res:
            return None
        return res[0]

    async def add_user(self,name,password):
        target=User(name=name,password=bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt()).decode())
        self.db.add(target)
        await self.db.commit()

    async def add_poll(self,title,options:list):
        target=Vote(title=title)
        self.db.add(target)
        await self.db.commit()
        await self.db.refresh(target)
        add_list=[target]
        ff=[]
        for i in options:
            target1=TypeVar(text=i, vote_id=target.id)
            ff.append(target1)
        add_list.extend(ff)
        self.db.add_all(add_list)
        await self.db.commit()

    async def get_all(self, CLASS, filters=None):
        ex=select(CLASS).filter(CLASS.id==filters if isinstance(filters,int)==True  else CLASS.id)
        res=(await self.db.execute(ex)).all()
        return res

    async def get_all_types(self, id, all=True):
            ex=select(TypeVar).filter(TypeVar.vote_id==id)
            res=(await self.db.execute(ex)).all() if all else (await self.db.execute(ex)).first()
            return res

    async def get_answer(self, user_id, vote_id):
            ex=select(Answer).filter(Answer.user_id==user_id, Answer.vote_id==vote_id)
            res=(await self.db.execute(ex)).first()
            if res:
                return res[0]
            else:
                return None



