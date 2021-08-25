import gql from 'graphql-tag'
import { apolloClient } from '../vue-apollo.js'

import omit from 'lodash/omit'

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
        name
      }
      sku
      upc
      price
      packQty: pack_qty
    }
  }
`

// export const ITEM_BY_ID_QUERY_DATA = async function () {
//   let data, errors
//   try {
//     data = await this.$apollo.query({
//       query: ITEM_BY_ID_QUERY,
//       variables: {
//         id: parseInt(this.itemId)
//       }
//     });
//     // shorten data and cast price and packQty to Float
//     data = data.data.itemById;
//     data.price = parseFloat(data.price);
//     data.packQty = parseFloat(data.packQty);
//   } catch (e) {
//     console.log(e.message);
//     errors = e.message;
//   }
//   // eslint-disable-next-line no-unsafe-finally
//   finally { return { data: data, errors: errors } }
// }

export async function itemByIdQueryData (id) {
  let data = null; let errors = {}
  try {
    const d = await apolloClient.query({
      query: ITEM_BY_ID_QUERY,
      variables: {
        id: id
      }
    })
    if (d.data.itemById) {
      // shorten data and cast price and packQty to Float
      data = d.data.itemById
      data.price = parseFloat(data.price)
      data.packQty = parseFloat(data.packQty)
      delete data.category.__typename

      // //remove __typename from payload
      // // https://github.com/apollographql/apollo-client/issues/1564#issuecomment-342163432
      data = omit(data, ['__typename'])
    }
  } catch (e) {
    errors = e.message
    console.log(errors)
  } finally {
    // eslint-disable-next-line no-unsafe-finally
    return { data: data, errors: errors }
  }
}

// export const ITEM_UPDATE_MUTATION = gql`
//   mutation updateItem($id: Int!, $input: ItemInputType!) {
//     updateItem: update_item(id: $id, input: $input) {
//       ok
//       errors
//       itemInstance: item_instance {
//         id
//         name
//       }
//     }
//   }
// `;

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
