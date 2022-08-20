from typing import List
from unittest import result

from core.database import Session
from core.deps import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.curso_model import CursoModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):

    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

    db.add(novo_curso)
    await db.commit()

    return novo_curso


@router.get("/", response_model=List[CursoModel])
async def get_curso(db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos


@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del = result.scalar_one_or_none()

        if curso_del:
            await session.delete(curso_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND
            )


@router.put(
    "/{curso_id}", response_model=CursoModel, status_code=status.HTTP_202_ACCEPTED
)
async def put_curso(
    curso_id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()

        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas

            await session.commit()
            return curso_up
        else:
            raise HTTPException(
                detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND
            )
