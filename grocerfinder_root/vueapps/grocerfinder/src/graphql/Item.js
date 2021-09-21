import gql from 'graphql-tag'
import {
  useQuery
  // useLazyQuery
} from '@vue/apollo-composable'
import { ref } from 'vue'

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
      category {
        id
        name
      }
      price
    }
  }
`

export const ITEM_FETCH_MORE_QUERY = gql`
  query itemFetchMore ($cursor: String!, $cursor_id: Int!, $page_size: Int!, $sort_by_field: String!) {
  itemFetchMore: item_fetch_more(cursor: $cursor, cursor_id: $cursor_id, page_size: $page_size, sort_by_field: $sort_by_field) {
    id
    name
    category {
      id
      name
    }
    price
  }
}
`

export function doItemFetchMore (cursor, cursorId, pageSize, sortByField) {
  const { onResult, loading, refetch, fetchMore } = useQuery(ITEM_FETCH_MORE_QUERY,
    {
      cursor: String(cursor),
      cursor_id: cursorId,
      page_size: pageSize,
      sort_by_field: sortByField
    },
    { fetchPolicy: 'no-cache' }
  )
  const data = ref({})
  onResult(result => {
    // test if result.data. exists
    if (result.data.itemFetchMore !== null) {
      data.value = result.data.itemFetchMore
      data.value.forEach(element => { element.category = element.category.name })
    }
  })
  return { data, loading, onResult, refetch, fetchMore }
}

// // trying with useLazyQuery
// // https://www.apollographql.com/docs/react/api/react/hooks/#uselazyquery
// // https://github.com/vuejs/vue-apollo/commit/8e95aea00fe5a9d01c290262c6684c7c3b615ab0
// export function doItemFetchMore (cursor, cursorId, pageSize, sortByField) {
//   const [getLazy, { onResult, loading, refetch }] = useLazyQuery(ITEM_FETCH_MORE_QUERY,
//     {
//       cursor: String(cursor),
//       cursor_id: cursorId,
//       page_size: pageSize,
//       sort_by_field: sortByField
//     },
//     { fetchPolicy: 'no-cache' }
//   )
//   const data = ref({})
//   onResult(result => {
//     // test if result.data. exists
//     if (result.data.itemFetchMore !== null) {
//       data.value = result.data.itemFetchMore
//       data.value.forEach(element => { element.category = element.category.name })
//     }
//   })
//   return { getLazy, data, loading, onResult, refetch }
// }

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

export function doItemFetchById (id) {
  const { onResult } = useQuery(ITEM_BY_ID_QUERY,
    { id: id },
    { fetchPolicy: 'no-cache' }
  )
  const isIdNotFound = ref({})
  onResult(result => {
    if (result.data.itemById !== null) {
      // test if result.data. exists
      isIdNotFound.value = false
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
mutation delete_item ($id_list: [Int]!) {
  deleteItem: delete_item (id_list: $id_list) {
    idDeleted: id_deleted
    idNotExist: id_not_exist
    errors
  }
}
`
