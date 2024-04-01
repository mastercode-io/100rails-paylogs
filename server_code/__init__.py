import anvil

app_env = anvil.AppEnvironment()
app_info = anvil.AppInfo()
print('app environment:', app_env.name, app_env.tags)
print('app info', app_info.branch, app_info.environment, app_info.id)
