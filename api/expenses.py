from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import engine, get_db
from models import User, Expense
from datetime import datetime, timedelta
from typing import List, Optional
from jose import JWTError, jwt
from auth import oauth2_scheme, get_current_user

router = APIRouter()

# JWT 토큰의 암호화에 사용할 시크릿 키
SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

# 지출 내역 조회 API
@router.get("/expenses", response_model=List[Expense])
def get_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    # 현재 사용자의 모든 지출 내역을 가져옵니다.
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).offset(skip).limit(limit).all()
    return expenses

# 지출 내역 상세 조회 API
@router.get("/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="지출 내역이 존재하지 않습니다.")
    return expense

# 지출 내역 등록 API
@router.post("/expenses", response_model=Expense)
def create_expense(expense: Expense, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_expense = Expense(user_id=current_user.id, amount=expense.amount, memo=expense.memo, created_at=datetime.now())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# 지출 내역 수정 API를 정의
@router.put("/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, expense: Expense, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not db_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="지출 내역이 존재하지 않습니다.")
    db_expense.amount = expense.amount
    db_expense.memo = expense.memo
    db.commit()
    db.refresh(db_expense)
    return db_expense

# 지출 내역 삭제 API
@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id ==current_user.id).first()
    if not db_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="지출 내역이 존재하지 않습니다.")
    db.delete(db_expense)
    db.commit()