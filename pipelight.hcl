pipelines = [
  {
    name = "fmt-n-lint"
    steps = [
      {
        name     = "format"
        commands = ["ruff format ranx"]
      },
      {
        name     = "lint"
        commands = ["ruff check ranx --fix"]
      }
    ]
    triggers = [{
      branches = ["main", "dev"]
      actions  = ["pre-commit"]
    }]
  }
]
