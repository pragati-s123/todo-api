## AI vs Me

**Prompt used:**
Built a simple CRUD API in Python using FastAPI for managing a to-do list of tasks, supporting create/list/get/update/delete, in-memory storage, 404 for missing tasks, 400 for missing/empty title, proper status codes (200/201/204), and Swagger UI docs.

**What the AI did better:**
Used Pydantic's built-in `field_validator` for title validation instead of manual if-checks, and used named status constants (`status.HTTP_201_CREATED`) instead of raw numbers — cleaner code style than mine.

**What it got wrong or silently ignored:**
Sending `POST /tasks` with an empty body `{}` returns **422**, not the 400 the assignment requires. Pydantic auto-rejects a missing `title` field before the AI's own custom validator even runs, so its "empty title" check never gets a chance to fire in this case.

**What my prompt forgot to specify:**
I didn't mention the `/` root endpoint or `/health` check endpoint at all, so the AI never built them — it only built what I explicitly described. It also didn't ask for a `.gitignore` or `__pycache__` handling, though that's minor.

**One-line change for the rematch:**
Added "title must always be required in the request; return 400 (not 422) if missing" explicitly to the prompt, since the AI needs to be told to override FastAPI's automatic validation behavior — it won't infer that on its own.