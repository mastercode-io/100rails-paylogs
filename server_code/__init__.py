from anvil import app

print('-- App Info --')
print(f'git branch: {app.branch}')
print(f'environment: {app.Environment.name} ({app.Environment.tags})')
print(f'id: {app.id}')
