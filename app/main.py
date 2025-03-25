from fastapi import FastAPI
from app.modules.auth.api.auth import router as auth_router
from app.modules.users.api.users import router as user_router
from app.modules.pia.api.pia import router as pia_router
from app.modules.analytics.api.analytics import router as analytics_router
from app.modules.admin.api.admin import router as admin_router

app = FastAPI(
    title="API - PIA Empresa",
    version="1.0.0",
    description="Hub de dados do Observatório da Indústria.",
)

# Rotas públicas e privadas
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(pia_router)
app.include_router(analytics_router)
app.include_router(admin_router)


