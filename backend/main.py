import tempfile
import shutil
import traceback
from fastapi import FastAPI, UploadFile, File

from review_agent import review_project

app = FastAPI(title="AI Code Review API")


@app.get("/")
def home():
    return {"message": "AI Code Review API Running"}


@app.post("/review")
async def review(file: UploadFile = File(...)):
    # Updated suffix configuration to handle tarball uploads from Jenkins
    temp_tar = tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz")

    try:
        print("\n========== REVIEW REQUEST ==========")
        print("Uploaded File:", file.filename)

        shutil.copyfileobj(file.file, temp_tar)
        temp_tar.close()

        # Call the review agent with our temporary tarball path
        result = review_project(temp_tar.name)

        return result

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        try:
            shutil.os.remove(temp_tar.name)
        except:
            pass
