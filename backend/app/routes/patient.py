from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user

router = APIRouter(
    prefix="/patient",
    tags=["Patient"]
)


@router.get("/dashboard")
def patient_dashboard(current_user=Depends(get_current_user)):

    if current_user["role"].lower() != "patient":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return {
    "message": f"Welcome {current_user['sub']}!"
}