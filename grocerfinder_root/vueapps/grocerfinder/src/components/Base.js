import { useRoute } from 'vue-router'

export function camelCaseToSentenceCase (string) {
  const result = string.replace(/([A-Z])/g, ' $1')
  return result.charAt(0).toUpperCase() + result.slice(1)
}
export function getModelIdFromRoute () {
  const id = useRoute().params.id
  return parseInt(id) || id
}
// return true if itemId is "new" string and false otherwise, i.e. an id
export function isModelIdNew (id) {
  return typeof id === 'string'
    ? id.toLowerCase() === 'create'
    : false
}
