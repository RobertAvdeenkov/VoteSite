from fastapi import APIRouter,Body,Cookie,Depends,HTTPException,Query
from fastapi.responses import* #type:ignore
import bcrypt
from database import *
from auth import *
from task_repo import*
from task_service import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import desc

router=APIRouter()

@router.get('/')
def root():
    return FileResponse('templates/reglog.html')

@router.post('/reglog')
async def reglog(data=Body(), db:AsyncSession=Depends(get_db)):
    repo=Repository(db)
    service=Service(repo)
    user=await service.check_get_user(data['name'])
    if not user:
        await service.check_add_user(data['name'], data['password'])
    elif not(bcrypt.checkpw(data['password'].encode(), user.password.encode())):
        raise HTTPException(401, 'Неправильный логин или пароль!')
    token=create_token(user.name if user else data['name'])
    return {'status':'ok', 'redirect_url':f'/mainpageRED?token={token}'}


@router.get('/mainpageRED')
async def mainpageRED(token=Query()):
    response=RedirectResponse('/mainpage')
    response.set_cookie(key='token', value=token, max_age=3600, path='/')
    return response

@router.get('/mainpage')
async def mainpage(token=Cookie(...)):
    get_by_token(token)
    return FileResponse('templates/mainpage.html')

@router.post('/polls')
async def create_poll(data=Body(), db:AsyncSession=Depends(get_db)):
    repo=Repository(db)
    service=Service(repo)
    await service.check_add_poll(data['title'], data['options'])

@router.post('/loadpolls')
async def load(db:AsyncSession=Depends(get_db), token=Cookie()):
    try:
        get_by_token(token)
        repo=Repository(db)
        service=Service(repo)
        ex=select(Vote).options(selectinload(Vote.typevar)).order_by(desc(Vote.created_at))
        result=(await db.execute(ex)).all()
        print(result)
        txt=''
        for i in result:
            print(i[0].title)
            txt+='<div class="poll">'
            txt+=f'    <h2>{i[0].title}</h2>'

            for index,j in enumerate(i[0].typevar):
                print(j.text,j.count)
                txt+='    <div style="display: flex;justify-content: space-between; align-items: center; margin-bottom: 12px; padding: 6px 0; border-bottom: 1px solid #444; color: #ffcc08; ">'
                txt+=f'        <h3>№{index+1}. {j.text} Число проголосовавших: {j.count}<h3><button onclick="vote({i[0].id},{j.id})">Выбрать</button><p></p>'
                txt+='    </div>'
            txt+='</div>'
        return {'message':txt}
    except Exception as e:
        print("ERROR!!!\t", e)

@router.post('/voting')
async def vote(data=Body(), db:AsyncSession=Depends(get_db), token=Cookie()):
    try:
        repo=Repository(db)
        service=Service(repo)
        name=get_by_token(token)
        user= await service.check_get_user(name)
        answer=await service.check_get_answer(user.id, data['pollID'])
        if answer: return {'voted':True}
        typ=(await db.execute(select(TypeVar).filter(TypeVar.id==int(data['typeID'])))).first()
        if not typ: raise HTTPException(400, 'Такого выбора нет')
        typp=typ[0]
        print(typp)
        typp.count+=1
        target=Answer(user_id=user.id, vote_id=data['pollID'])
        db.add(target)
        await db.commit()
        return {'voted':False}
    except Exception as e:
        print(e)