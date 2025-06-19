resource "aws_secretsmanager_secret" "api_key" {
  name = "api-key"
  description = "API key for authenticating requests to my FastAPI app"
}
  
resource "aws_secretsmanager_secret_version" "api_key_version" {
  secret_id     = aws_secretsmanager_secret.api_key.id
  secret_string = jsonencode({
    key = "api-key-123"
  })
}