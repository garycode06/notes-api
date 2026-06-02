from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def get_all_items():
    return {'message': 'Succesful'}