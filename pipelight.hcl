pipelines = [
  {
    name = "fmt-n-lint"
    steps = [
      {
        name     = "format"
        commands = ["ruff format ranlibx"]
      },
      {
        name     = "lint"
        commands = ["ruff check ranlibx --fix"]
      }
    ]
    triggers = [{
      branches = ["main", "dev"]
      actions  = ["pre-commit"]
    }]
  }
]
