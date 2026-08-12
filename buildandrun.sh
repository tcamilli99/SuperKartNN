cd backend
docker build -t superkart-nn-backend .
cd ../frontend
docker build -t superkart-nn-frontend .
docker network create superkart-nn-network
docker run -d --name backend --network superkart-nn-network -p 7860:7860 superkart-nn-backend
docker run -d --name frontend --network superkart-nn-network -p 8501:8501 superkart-nn-frontend
