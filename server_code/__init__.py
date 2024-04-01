from anvil import app

print('--- App Info ---')
print(f'git branch: {app.branch}')
print(f'environment: {app.environment.name} ({app.environment.tags})')
print(f'id: {app.id}')
