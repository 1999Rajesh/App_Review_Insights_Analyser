# Deploy backend to Railway with Docker
cd backend

# Login to Railway CLI (if not already logged in)
railway login

# Link to your Railway project
railway link

# Deploy with Docker
railway up --dockerfile Dockerfile
