<template>
  <div v-if="!$apollo.loading">
    <!-- <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th></th>
          <th>ID</th>
          <th>Item Name</th>
          <th>Category</th>
        </tr>
      </thead>
      <tbody>
        <item-table-row
          v-for="item in allItems"
          :key="item.id"
          :id="item.id"
          :name="item.name"
          :category="item.category.name"
          @checkbox-changed="changeCheckbox(item.id)"
        ></item-table-row>
      </tbody>
    </table> -->

    <button @click="deleteItem" class="btn btn-danger">Delete</button>
    <router-link :to="`/item/create`"
      ><button class="btn btn-primary">New Item</button></router-link
    >
    <p v-if="message.length > 0">{{ message }}</p>
    <raw-data-table
      :tableData="allItems"
      :checkedBox="checkedBox"
      @checkbox-changed="changeCheckbox"
      @deleteEntry="deleteItem"
    ></raw-data-table>
  </div>
</template>

<script>
import { ALL_ITEMS_QUERY, ITEM_DELETE_MUTATION } from '../graphql/Item.js'
// import ItemTableRow from "./ItemTableRow.vue";
import RawDataTable from '../components/RawDataTable.vue'

export default {
  name: 'AllItems',
  data: function () {
    return {
      allItems: [],
      checkedBox: [],
      ITEM_DELETE_MUTATION: ITEM_DELETE_MUTATION,
      ALL_ITEMS_QUERY: ALL_ITEMS_QUERY,
      message: []
    }
  },
  components: {
    // ItemTableRow,
    RawDataTable
  },
  apollo: {
    allItems: {
      query: ALL_ITEMS_QUERY
    }
  },
  methods: {
    changeCheckbox (id) {
      const pos = this.checkedBox.indexOf(id)
      if (pos === -1) {
        this.checkedBox.push(id)
      } else {
        this.checkedBox.splice(pos, 1)
      }
    },
    // Use this instead of MutationComponent as the logic is complex
    async deleteItem () {
      if (this.checkedBox.length > 0) {
        try {
          let data = await this.$apollo.mutate({
            mutation: ITEM_DELETE_MUTATION,
            variables: {
              id_list: this.checkedBox
            },
            refetchQueries: [
              {
                query: ALL_ITEMS_QUERY
              }
            ]
          })
          this.message = []
          data = data.data.deleteItem
          // Removed id deleted in idDeleted array from this.checkedBox array
          this.checkedBox = this.checkedBox.filter(
            id => !data.idDeleted.includes(id)
          )
          // Removed id not exist in idNotExist array from this.checkedBox array
          this.checkedBox = this.checkedBox.filter(
            id => !data.idNotExist.includes(id)
          )
          // console.log(data.idDeleted, this.checkedBox);
          if (data.idDeleted.length > 0) {
            this.message.push('Deleted id(s) ' + data.idDeleted + ' OK')
          }

          if (data.errors.length > 0) {
            this.message.push(...data.errors)
          }
        } catch (e) {
          // console.log(e.message);
          this.message.push(...e)
        }
      }
    }
  },
  computed: {
    // allItemsConvertCategory: function() {
    //   for (let item of this.allItems) {
    //     item.category = item.category.name;
    //   }
    //   return this.allItems;
    // }
  }
}
</script>
