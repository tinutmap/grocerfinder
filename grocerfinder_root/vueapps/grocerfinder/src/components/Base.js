export function camelCaseToPascalCase (string) {
  const result = string.trim().replace(/([A-Z])/g, ' $1')
  return result.charAt(0).toUpperCase() + result.slice(1)
}

export function toPascalCase (string) {
  const result = string.trim().toLowerCase()
  return result.charAt(0).toUpperCase() + result.slice(1)
}

export function getModelIdFromRoute (route) {
  if (route.params.id) {
    const id = route.params.id
    return parseInt(id) || id
  } else {
    return undefined
  }
}

// return true if itemId is "/create" string and false otherwise, i.e. an id
export function isModelIdNew (id) {
  return typeof id === 'string'
    ? id.toLowerCase() === 'create'
    : false
}
