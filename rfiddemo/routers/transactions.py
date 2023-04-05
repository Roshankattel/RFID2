from fastapi import status, HTTPException, Depends, APIRouter
from database import SessionLocal
from sqlmodel import Session
import models, schemas, utils, oauth2
from typing import List, Optional
router = APIRouter(
    prefix="/transactions",
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.TransactionResponse)
def create_transaction (transaction :schemas.TransactionCreate,
                 current_merchant: int = Depends(oauth2.get_current_merchant)):

    user_query = SessionLocal.query(models.User).filter(models.User.tag_data==transaction.tag_data)
    user = user_query.first()
    if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with given tag_id not found")

    if not transaction.recharge_request: 
        if (user.amount < transaction.amount):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Not enough balance with user")
        user.amount = user.amount-transaction.amount
    else :
        user.amount = user.amount+transaction.amount

    #update amount of merchant 
    merchant_query = SessionLocal.query(models.Merchant).filter(models.Merchant.id==current_merchant.id)
    merchant = merchant_query.first()
    if transaction.recharge_request:  
        if  merchant.amount < transaction.amount:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f"Not enough balance with Merchant")
        merchant.amount = merchant.amount - transaction.amount
    else:
        merchant.amount = merchant.amount + transaction.amount
    new_transaction = models.Transaction(merchant_id= current_merchant.id, user_id = user.id, amount = transaction.amount, recharge_request=transaction.recharge_request)
    SessionLocal.add(new_transaction)
    SessionLocal.commit()
    SessionLocal.refresh(new_transaction)
    
    return(new_transaction)


@router.get("/{id}", response_model=List[schemas.TransactionResponse])
def get_transactions(id:int):
    user = SessionLocal.query(models.User).filter(models.User.id == id).first()
    print(user.transactions)
    if not user.transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id:{id} was not found")
    return user.transactions

@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int):
   transaction = SessionLocal.query(models.Transaction).filter(models.Transaction.id == id).first()
   print
   if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id:{id} was not found")
   return transaction.user

@router.get("/users/merchats/{id}", response_model=List[schemas.MerchantResponse])
def get_user_merchant(id:int):
    user = SessionLocal.query(models.User).filter(models.User.id == id).first()
    print(user.merchants)
    if not user.merchants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id:{id} was not found")
    return user.merchants


@router.get("/merchants/users/{id}", response_model=List[schemas.UserResponse])
def get_merchants_user(id:int):
    merchants = SessionLocal.query(models.Merchant).filter(models.Merchant.id == id).first()
    print(merchant.users)
    if not merchants.user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id:{id} was not found")
    return merchant.users




