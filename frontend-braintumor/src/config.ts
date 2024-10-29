const loadEnvironmentValue = (key: string) => {
  const value = import.meta.env[key]

  if (!value) {
    throw new Error(`Missing environment variable ${key}`)
  }

  return value
}

export const config = {
  backendURL: loadEnvironmentValue('VITE_BACKEND_URL'),
}
