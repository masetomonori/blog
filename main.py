from fastapi import FastAPI
from models import Base
from database import engine
from routes import blog, user, auth
from schemas import Pxe

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)

Base.metadata.create_all(engine)

@app.get('/')
def index():
    #return '"hello"'
    power_status = {"@odata.id":"\/redfish\/v1\/Managers\/iRMC\/Oem\/ts_fujitsu\/iRMCConfiguration\/PowerStatusSummary","@odata.type":"#FTSPowerStatusSummary.v1_0_3.FTSPowerStatusSummary","Name":"Power Status Summary","PowerStatus":"On","PowerOnTimeMin":1009935,"LastPowerOnReason":"Software","LastPowerOffReason":"Software","@Redfish.Copyright":"Copyright 2017-2020 FUJITSU LIMITED","@odata.etag":"1662602430"}
    return power_status

@app.patch('/pxe')
def patch(request: Pxe):
    return request

 
