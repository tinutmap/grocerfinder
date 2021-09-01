import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'

export const ITEM_CREATE_BY_FORM_MUTATION = gql`
mutation item_create_by_form ($ItemFormCreateMutationInput: ItemFormCreateMutationInput!){
  itemCreateByForm: item_create_by_form (input: $ItemFormCreateMutationInput) {
    item {
      id
      name
    }
    errors {
      field
      messages
    }
    # ok
  }
}
`

export const ALL_ITEMS_QUERY = gql`
  query all_items {
    allItems: all_items {
      id
      name
      # category {
      #   id
      #   name
      # }
    }
  }
`

export const ITEM_BY_ID_QUERY = gql`
  query itemById($id: Int!) {
    itemById: item_by_id(id: $id) {
      name
      category {
        id
        # name
      }
      sku
      upc
      price
      packQty: pack_qty
    }
  }
`

export function fetchItemById (id) {
  const { onResult } = useQuery(ITEM_BY_ID_QUERY,
    { id: id },
    { fetchPolicy: 'no-cache' }
  )
  const isIdNotFound = { value: false }
  onResult(result => {
    if (result.data.itemById !== null) {
      // test if result.data. exists
      result = result.data.itemById
      result.price = parseFloat(result.price)
      result.packQty = parseFloat(result.packQty)
    } else {
      isIdNotFound.value = true
    }
  })
  return { onResult, isIdNotFound }
}

export const ITEM_UPDATE_BY_FORM_MUTATION = gql`mutation item_update_by_form ($ItemFormUpdateMutationInput: ItemFormUpdateMutationInput!){
  itemUpdateByForm: item_update_by_form(input: $ItemFormUpdateMutationInput) {
    item {
      id
      name
    }
    errors {
      field
      messages
    }
    ok
  }
}
`

export const ITEM_DELETE_MUTATION = gql`
mutation deleteItem ($id_list: [Int]!) {
  deleteItem: delete_item (id_list: $id_list) {
    idDeleted: id_deleted
    idNotExist: id_not_exist
    errors
  }
}
`
