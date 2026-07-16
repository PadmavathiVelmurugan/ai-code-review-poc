from fastapi import FastAPI, UploadFile, File
import tempfile
import shutil
import traceback

from review_agent import review_project

app = FastAPI(title="AI Code Review API")


@app.get("/")
def home():
    return {"message": "AI Code Review API Running"}


@app.post("/review")
async def review(file: UploadFile = File(...)):
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")

    try:
        print("\n========== REVIEW REQUEST ==========")
        print("Uploaded File:", file.filename)

        shutil.copyfileobj(file.file, temp_zip)
        temp_zip.close()

        result = review_project(temp_zip.name)

        return result

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        try:
            shutil.os.remove(temp_zip.name)
        except:
            pass