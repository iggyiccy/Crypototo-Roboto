terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.48.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.2.0"
    }
  }

  required_version = "~> 1.0"
}

provider "aws" {
  region = var.aws_region
}

resource "random_pet" "lambda_bucket_name" {
  prefix = "trading-signal"
  length = 4
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = random_pet.lambda_bucket_name.id

  acl           = "private"
  force_destroy = true
  versioning {
    enabled = true
  }
}

data "archive_file" "lambda_trading_signal" {
  type = "zip"

  source_dir  = "${path.module}/signal_function"
  output_path = "${path.module}/signal_function.zip"
}

resource "aws_s3_bucket_object" "lambda_trading_signal" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "signal_function.zip"
  source = data.archive_file.lambda_trading_signal.output_path

  etag = filemd5(data.archive_file.lambda_trading_signal.output_path)
}

resource "aws_sqs_queue" "binance_sqs_queue_deadletter" {
  name = "websocket_stream_binance_ethusdc_deadletter"
  delay_seconds = 90
  max_message_size = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
}

resource "aws_sqs_queue" "binance_sqs_queue" {
  name                      = "websocket_stream_binance_ethusdc"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.binance_sqs_queue_deadletter.arn
    maxReceiveCount     = 4
  })
  tags = {
    Environment = "production"
  }
}