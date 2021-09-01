import gql from 'graphql-tag'
import { apolloClient } from '../vue-apollo.js'
import { useQuery, useResult } from '@vue/apollo-composable'
// import { cloneDeep } from 'lodash'

export const CATEGORY_CREATE_BY_FORM_MUTATION = gql`
  mutation category_create_by_form(
    $CategoryFormCreateMutationInput: CategoryFormCreateMutationInput!
  ) {
    categoryCreateByForm: category_create_by_form(input: $CategoryFormCreateMutationInput) {
      category {
        id
        name
        datetime_updated
      }
      errors {
        field
        messages
      }
      ok
    }
  }
`
export const ALL_CATEGORIES_QUERY = gql`
  query all_categories {
    allCategories: all_categories {
      id
      name
      datetimeUpdated: datetime_updated
    }
  }
`

export async function categoryAllQueryData () {
  let data = null; let errors = {}
  try {
    const d = await apolloClient.query({
      query: ALL_CATEGORIES_QUERY
    })
    if (d.data.allCategories) {
      data = d.data.allCategories
    }
  } catch (e) {
    errors = e.message
    console.log(errors)
  } finally {
    // eslint-disable-next-line no-unsafe-finally
    return { data: data, errors: errors }
  }
}

export function fetchCategoryAll () {
  const { result, loading, refetch } = useQuery(ALL_CATEGORIES_QUERY, null, { fetchPolicy: 'no-cache' })
  const data = useResult(result, null, data => data.allCategories)
  return { data, loading, refetch }
}

export const CATEGORY_BY_ID_QUERY = gql`
  query categoryById($id: Int!) {
    categoryById: category_by_id(id: $id) {
      name
    }
  }
`

// export async function categoryByIdQueryData (id) {
//   let data = null; let errors = {}
//   try {
//     const d = await apolloClient.query({
//       query: CATEGORY_BY_ID_QUERY,
//       variables: {
//         id: id
//       }
//     })
//     if (d.data.categoryById) {
//       data = cloneDeep(d.data.categoryById)
//     }
//   } catch (e) {
//     errors = e.message
//     console.log(errors)
//   } finally {
//     // eslint-disable-next-line no-unsafe-finally
//     return { data: data, errors: errors }
//   }
// }

export function fetchCategoryById (id) {
  const { onResult } = useQuery(CATEGORY_BY_ID_QUERY,
    { id: id },
    { fetchPolicy: 'no-cache' }
  )
  const isIdNotFound = { value: false }
  onResult(result => {
    // test if result.data. exists
    if (result.data.categoryById) {
      result = result.data.categoryById
    } else {
      isIdNotFound.value = true
    }
  })
  return { onResult, isIdNotFound }
}

export const CATEGORY_UPDATE_BY_FORM_MUTATION = gql`
  mutation category_update_by_form(
    $CategoryFormUpdateMutationInput: CategoryFormUpdateMutationInput!
  ) {
    categoryUpdateByForm: category_update_by_form(input: $CategoryFormUpdateMutationInput) {
      category {
        id
        name
        datetime_updated
      }
      errors {
        field
        messages
      }
      ok
    }
  }
`

export const CATEGORY_DELETE_MUTATION = gql`
  mutation delete_category($id_list: [Int]!) {
    deleteCategory: delete_category(id_list: $id_list) {
      idDeleted: id_deleted
      errors
      idNotExist: id_not_exist
    }
  }
`
