<template>
  <!-- Checking if data is fully loaded before rendering -->
  <div v-if="!$apollo.loading">
    <p
      v-for="i in okMessage"
      :key="i.key"
      :value="i.value"
      class="alert alert-success"
    >
      {{ i }}
    </p>
    <p
      v-for="i in errorMessage"
      :key="i.key"
      :value="i.value"
      class="alert alert-danger"
    >
      {{ i }}
    </p>
    <div>
      <span>Category Name:</span>
      <input type="text" v-model="categoryName" />
      <router-link :to="`category/create`" append>
        <button>Create</button>
      </router-link>
      <!-- <apollo-mutation
        :mutation="gql => CATEGORY_CREATE_BY_FORM_MUTATION"
        :variables="{
          CategoryFormCreateMutationInput: {
            name: categoryName
          }
        }"
        :refetchQueries="() => [{ query: ALL_CATEGORIES_QUERY }]"
      >
        <template v-slot="{ mutate, loading, error, gqlError }">
          <button :disabled="loading" @click="mutate()" class="btn btn-primary">
            Add Category
          </button>
          <p v-if="error">{{ error }}</p>
          <p v-else>{{ okMessage }}</p>
          <p v-if="gqlError">gql: {{ gqlError }}</p>
        </template>
      </apollo-mutation> -->
    </div>
    <div>
      <!-- <table>
        <tr>
          <th></th>
          <th>ID</th>
          <th>Catergory Name</th>
          <th>Date Updated</th>
        </tr>
        <category-table-row
          v-for="category in allCategories"
          :key="category.id"
          :id="category.id"
          :name="category.name"
          :datetimeUpdated="category.datetimeUpdated"
          @checkbox-changed="changeCheckbox(category.id)"
        ></category-table-row>
      </table> -->
      <!-- <button @click="deleteCategory()">Delete</button> -->

      <raw-data-table
        :tableData="allCategoriesDateTimeUpdatedCast"
        :checkedBox="checkedBox"
        @checkbox-changed="changeCheckbox"
        @deleteEntry="deleteCategory"
      ></raw-data-table>

      <router-link :to="`create`" append>
        <button class="btn btn-primary">Create</button>
      </router-link>
      <button @click="deleteCategory(checkedBox)" class="btn btn-danger">
        Delete
      </button>
    </div>
  </div>
</template>

<script>
import {
  // CATEGORY_CREATE_MUTATION,
  CATEGORY_DELETE_MUTATION,
  // ALL_CATEGORIES_QUERY,
  // categoryAllQueryData,
  // CATEGORY_UPDATE_MUTATION,
  CATEGORY_CREATE_BY_FORM_MUTATION
} from '../graphql/Category.js'

import CategoryGql from '../graphql/Category.vue'

import RawDataTable from '../components/RawDataTable.vue'

// eslint-disable-next-line no-unused-vars
import omit from 'lodash/omit'

export default {
  name: 'CategoryAll',
  mixins: [CategoryGql],
  data () {
    return {
      categoryName: undefined,
      id: undefined,
      checkedBox: [],
      allCategories: [],
      CATEGORY_CREATE_BY_FORM_MUTATION: CATEGORY_CREATE_BY_FORM_MUTATION,
      // ALL_CATEGORIES_QUERY: ALL_CATEGORIES_QUERY,
      okMessage: [],
      errorMessage: [],
      loading: false
    }
  },
  // apollo: {
  //   allCategories: {
  //     query: ALL_CATEGORIES_QUERY,
  //     update: function(data) {
  //       if (data.allCategories) {
  //         return data.allCategories.map(i => omit(i, ["__typename"]));
  //       }
  //     }
  //   }
  // },
  // async created() {
  // this.loading = true;
  // const data = await this.categoryAllQueryData();
  // if (data.data) {
  //   this.allCategories = data.data;
  //   // this.nonFieldErrors = data.errors;
  // } else {
  //   //https://github.com/vuejs/vue-router/issues/724 for fixing warning
  //   this.$router.replace({ name: "notFound404" });
  // }
  // this.loading = false;
  // },
  components: {
    // CategoryTableRow,
    RawDataTable
  },
  methods: {
    // async create_category() {
    //   const categoryName = this.categoryName;
    //   const data = await this.$apollo.mutate({
    //     mutation: CATEGORY_CREATE_MUTATION,
    //     variables: {
    //       input: {
    //         name: categoryName
    //       }
    //     },
    //     refetchQueries: [
    //       {
    //         query: ALL_CATEGORIES_QUERY
    //       }
    //     ]
    //     // This way below does not make the latest update category to top per query design in django
    //     // update: (store, { data: { createCategory } }) => {
    //     //   // Add to All Category list
    //     //   const data = store.readQuery({ query: ALL_CATEGORIES_QUERY });
    //     //   data.allCategories.push(createCategory.categories);
    //     //   store.writeQuery({ query: ALL_CATEGORIES_QUERY, data });
    //     // }
    //   });
    //   var t = data.data.createCategory.categoryInstance;
    //   console.log("Added ", t, "ok");
    //   this.categoryName = "";
    //   this.description = "";
    // },
    // update_category(id) {
    //   console.log(`Update category: # ${id}`);
    //   this.$apollo.mutate({
    //     mutation: CATEGORY_UPDATE_MUTATION,
    //     variables: {
    //       id: id
    //     }
    //   });
    // },
    changeCheckbox (id) {
      const pos = this.checkedBox.indexOf(id)
      // if id not in checkedBox array, i.e. pos === -1
      if (pos === -1) {
        this.checkedBox.push(id)
      } else {
        this.checkedBox.splice(pos, 1)
      }
      // this.checkedBox = id;
    },

    // async deleteCategory() {
    //   // remove id 1 from checkedBox since 1 can't be deleted
    //   let index1 = this.checkedBox.indexOf(1);
    //   if (index1 > -1) {
    //     this.checkedBox.splice(index1, 1);
    //     // document.getElementById("rawDataTableCheckBox1").checked = false;
    //   }

    //   if (this.checkedBox.length > 0) {
    //     try {
    //       let data = await this.$apollo.mutate({
    //         mutation: CATEGORY_DELETE_MUTATION,
    //         variables: {
    //           id_list: this.checkedBox
    //         },
    //         refetchQueries: [
    //           {
    //             query: ALL_CATEGORIES_QUERY
    //           }
    //         ]
    //       });
    //       //   const idDeleted = data.data.deleteCategory.idDeleted;
    //       //   // Removed id deleted in idDeleted array from this.checkedBox array
    //       //   this.checkedBox = this.checkedBox.filter(
    //       //     id => !idDeleted.includes(id)
    //       //   );
    //       //   console.log(idDeleted, this.checkedBox);
    //       // } catch (e) {
    //       //   console.log(e.okMessage);
    //       // }

    //       this.okMessage = [];
    //       data = data.data.deleteCategory;
    //       // Removed id deleted in idDeleted array from this.checkedBox array
    //       this.checkedBox = this.checkedBox.filter(
    //         id => !data.idDeleted.includes(id)
    //       );
    //       // data.idDeleted.forEach(id => {
    //       //   document.getElementById(
    //       //     "rawDataTableCheckBox" + id
    //       //   ).checked = false;
    //       // });
    //       // Removed id not exist in idNotExist array from this.checkedBox array
    //       this.checkedBox = this.checkedBox.filter(
    //         id => !data.idNotExist.includes(id)
    //       );
    //       // data.idNotExist.forEach(id => {
    //       //   document.getElementById(
    //       //     "rawDataTableCheckBox" + id
    //       //   ).checked = false;
    //       // });
    //       // console.log(data.idDeleted, this.checkedBox);
    //       if (data.idDeleted.length > 0) {
    //         this.okMessage.push("Deleted id(s) " + data.idDeleted + " OK");
    //       }

    //       if (data.errors.length > 0) {
    //         this.okMessage.push(...data.errors);
    //       }
    //     } catch (e) {
    //       // console.log(e.okMessage);
    //       this.okMessage.push(...e);
    //     }
    //   }
    // },
    async deleteCategory (idArray) {
      this.okMessage = []
      // remove id 1 from checkedBox since 1 can't be deleted
      const index1 = idArray.indexOf(1)
      if (index1 > -1) {
        idArray.splice(index1, 1)
        this.errorMessage = []
        this.errorMessage.push("Item 'default' can't be deleted")
        // document.getElementById("rawDataTableCheckBox1").checked = false;
      }

      if (idArray.length > 0) {
        try {
          let data = await this.$apollo.mutate({
            mutation: CATEGORY_DELETE_MUTATION,
            variables: {
              id_list: idArray
            },
            refetchQueries: [
              {
                // eslint-disable-next-line no-undef
                query: this.ALL_CATEGORIES_QUERY
              }
            ]
          })
          //   const idDeleted = data.data.deleteCategory.idDeleted;
          //   // Removed id deleted in idDeleted array from this.checkedBox array
          //   this.checkedBox = this.checkedBox.filter(
          //     id => !idDeleted.includes(id)
          //   );
          //   console.log(idDeleted, this.checkedBox);
          // } catch (e) {
          //   console.log(e.okMessage);
          // }

          // //refetch
          // const d = await this.categoryAllQueryData();
          // this.allCategories = d.data;

          this.okMessage = []
          data = data.data.deleteCategory
          // Removed id deleted in idDeleted array from this.checkedBox array
          this.checkedBox = this.checkedBox.filter(
            id => !data.idDeleted.includes(id)
          )
          // data.idDeleted.forEach(id => {
          //   document.getElementById(
          //     "rawDataTableCheckBox" + id
          //   ).checked = false;
          // });
          // Removed id not exist in idNotExist array from this.checkedBox array
          this.checkedBox = this.checkedBox.filter(
            id => !data.idNotExist.includes(id)
          )
          // data.idNotExist.forEach(id => {
          //   document.getElementById(
          //     "rawDataTableCheckBox" + id
          //   ).checked = false;
          // });
          // console.log(data.idDeleted, this.checkedBox);
          if (data.idDeleted.length > 0) {
            this.okMessage.push('Deleted id(s) ' + data.idDeleted + ' OK')
          }

          if (data.errors.length > 0) {
            this.errorMessage.push(...data.errors)
          }
        } catch (e) {
          this.errorMessage.push(...e)
        }
      }
    }
  },
  computed: {
    allCategoriesDateTimeUpdatedCast: function () {
      // cast datetimeUpdated from String to ISOString
      const t = this.allCategories
      // let i;
      // for (i of Object.keys(t)) {
      //   t[i].datetimeUpdated = new Date(t[i].datetimeUpdated).toString();
      // }
      // t.map(i => (i.datetimeUpdated = new Date(i.datetimeUpdated).toString()));
      return t
    }
  }
}
</script>
