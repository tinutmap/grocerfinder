<script>
import gql from 'graphql-tag'
// import {
//   // createProvider,
//   defaultOptions
// } from "../vue-apollo.js";
// import { createApolloClient } from "vue-cli-plugin-apollo/graphql-client";

// import { omit-deep} from "lodash/omit-deep";
import omit from 'lodash/omit'

// eslint-disable-next-line no-unused-vars
// const { apolloClient, wsClient } = createApolloClient({
//   ...defaultOptions
// });

// const ac = createProvider().apolloClient

// export const CATEGORY_CREATE_MUTATION = gql`
//   mutation create_category($input: CategoryInputType!) {
//     createCategory: create_category(input: $input) {
//       ok
//       errors
//       categoryInstance: category_instance {
//         id
//         name
//         datetimeUpdated: datetime_updated
//       }
//     }
//   }
// `;

export const CATEGORY_CREATE_BY_FORM_MUTATION = gql`
  mutation category_create_by_form(
    $CategoryFormCreateMutationInput: CategoryFormCreateMutationInput!
  ) {
    categoryCreateByForm: category_create_by_form(
      input: $CategoryFormCreateMutationInput
    ) {
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
const ALL_CATEGORIES_QUERY = gql`
  query all_categories {
    allCategories: all_categories {
      id
      name
      datetimeUpdated: datetime_updated
    }
  }
`

// export async function categoryAllQueryData() {
//   let data = null,
//     errors = {};
//   try {
//     const d = await apolloClient.query({
//       query: ALL_CATEGORIES_QUERY
//     });
//     if (d.data.allCategories) {
//       data = d.data.allCategories.map(i => omit(i, ["__typename"]));
//     }
//   } catch (e) {
//     errors = e.message;
//     console.log(errors);
//   } finally {
//     // eslint-disable-next-line no-unsafe-finally
//     return { data: data, errors: errors };
//   }
// }

export const CATEGORY_BY_ID_QUERY = gql`
  query category_by_id($id: Int!) {
    categoryById: category_by_id(id: $id) {
      name
    }
  }
`

// export async function categoryByIdQueryData(id) {
//   let data = null,
//     errors = {};
//   try {
//     const d = await apolloClient.query({
//       query: CATEGORY_BY_ID_QUERY,
//       variables: {
//         id: id
//       }
//     });
//     if (d.data.categoryById) {
//       data = d.data.categoryById;
//       //remove __typename from payload
//       // https://github.com/apollographql/apollo-client/issues/1564#issuecomment-342163432
//       data = omit(data, ["__typename"]);
//     }
//   } catch (e) {
//     errors = e.message;
//     console.log(errors);
//   } finally {
//     // eslint-disable-next-line no-unsafe-finally
//     return { data: data, errors: errors };
//   }
// }

// export const CATEGORY_UPDATE_MUTATION = gql`
//   mutation updateCategory($id: Int!, $input: CategoryInputType!) {
//     updateCategory: update_category(id: $id, input: $input) {
//       query {
//         all_categories {
//           id
//           name
//           datetimeUpdated: datetime_updated
//         }
//       }
//     }
//   }
// `;

export const CATEGORY_UPDATE_BY_FORM_MUTATION = gql`
  mutation category_update_by_form(
    $CategoryFormUpdateMutationInput: CategoryFormUpdateMutationInput!
  ) {
    categoryUpdateByForm: category_update_by_form(
      input: $CategoryFormUpdateMutationInput
    ) {
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

// export const CATEGORY_DELETE_MUTATION = gql`
//   mutation delete_category($id: Int!) {
//     deleteCategory: delete_category(id: $id) {
//       ok
//       errors
//       categoryInstance: category_instance {
//         id
//         name
//       }
//     }
//   }
// `;

export const CATEGORY_DELETE_MUTATION = gql`
  mutation delete_category($id_list: [Int]!) {
    deleteCategory: delete_category(id_list: $id_list) {
      idDeleted: id_deleted
      errors
      idNotExist: id_not_exist
    }
  }
`
export default {
  name: 'CategoryGql',
  data: function () {
    return {
      ALL_CATEGORIES_QUERY: ALL_CATEGORIES_QUERY
    }
  },
  methods: {
    async categoryAllQueryData () {
      let data = null
      let errors = {}
      try {
        const d = await this.$apollo.query({
          query: ALL_CATEGORIES_QUERY,
          variables: {}
        })
        if (d.data.allCategories) {
          data = d.data.allCategories.map(i => omit(i, ['__typename']))
        }
      } catch (e) {
        errors = e.message
        console.log(errors)
      } finally {
        // eslint-disable-next-line no-unsafe-finally
        return { data: data, errors: errors }
      }
    }
  },
  apollo: {
    allCategories: {
      query: ALL_CATEGORIES_QUERY,
      update: function (data) {
        if (data.allCategories) {
          return data.allCategories.map(i => omit(i, ['__typename']))
        }
      }
    }
  }
}
</script>
