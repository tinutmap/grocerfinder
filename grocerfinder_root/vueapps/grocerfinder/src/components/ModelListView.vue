<template>
  <div>
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
    <!-- to-do: put Create and Delete button into template or render function for DRY -->
    <router-link :to="$route.path + '/create'">
      <button class="btn btn-primary">Create</button>
    </router-link>
    <button @click="deleteObject(checkedBox)" class="btn btn-danger">
      Delete
    </button>
    <label for="pageSize">Result Qty</label>
    <select
      name=""
      id="pageSize"
      :value="pageSize"
      @input="$emit('update:pageSize', parseInt($event.target.value))"
    >
      <option
        v-for="size in pageSizeOptions"
        :key="size"
        :value="size"
        :selected="pageSize"
      >
        {{ size }}
      </option>
    </select>
    <label for="sortByField">Sort By</label>
    <select
      name=""
      id="sortByField"
      :value="sortByField"
      @input="$emit('update:sortByField', $event.target.value)"
    >
      <option
        v-for="field in sortedFields"
        :key="field"
        :value="field"
        :selected="sortByField"
      >
        {{ field }}
      </option>
    </select>
    <raw-data-table
      :tableData="modelData"
      :checkedBox="checkedBox"
      @checkbox-changed="changeCheckbox"
      @deleteEntry="deleteObject"
    ></raw-data-table>

    <router-link :to="$route.path + '/create'">
      <button class="btn btn-primary">Create</button>
    </router-link>
    <button @click="deleteObject(checkedBox)" class="btn btn-danger">
      Delete
    </button>
    <button @click="this.$emit('doFetchMore')" class="btn btn-primary">
      Load More
    </button>
    <button @click="testThis" class="btn btn-danger">
      Test This from Child Component
    </button>
  </div>
</template>

<script>
import RawDataTable from './RawDataTable.vue'
import { toPascalCase } from './Base.js'
export default {
  name: 'ModelListView',
  data () {
    return {
      //   categoryName: undefined,
      //   id: undefined,
      checkedBox: [],
      okMessage: [],
      errorMessage: [],
      pageSizeOptions: [5, 10, 25, 50, 100]
    }
  },
  components: {
    RawDataTable
  },
  props: [
    'modelName',
    'modelData',
    'deleteMutation',
    // 'refetch',
    'sortedFields',
    'doModelFetchMore',
    'sortByField',
    'pageSize'
  ],
  methods: {
    changeCheckbox (id) {
      const pos = this.checkedBox.indexOf(id)
      // if id not in checkedBox array, i.e. pos === -1
      if (pos === -1) {
        this.checkedBox.push(id)
      } else {
        this.checkedBox.splice(pos, 1)
      }
    },
    async deleteObject (idArray) {
      this.okMessage = []
      // remove id 1 from checkedBox since 1 can't be deleted
      const index1 = idArray.indexOf(1)
      if (index1 > -1) {
        idArray.splice(index1, 1)
        this.errorMessage = []
        this.errorMessage.push("Item 'default' can't be deleted")
      }

      if (idArray.length > 0) {
        try {
          let data = await this.$apollo.mutate({
            mutation: this.deleteMutation,
            variables: {
              id_list: idArray
            }
          })
          //   const data = {}
          //   asyncFn().then((d) => { data.value = d.data.deleteItem })
          this.refetch()
          this.okMessage = []
          data = data.data['delete' + this.modelNameToPascalCase]
          // Removed id deleted in idDeleted array from this.checkedBox array
          this.checkedBox = this.checkedBox.filter(
            id => !data.idDeleted.includes(id)
          )
          // Removed id not exist in idNotExist array from this.checkedBox array
          this.checkedBox = this.checkedBox.filter(
            id => !data.idNotExist.includes(id)
          )
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
    },
    async testThis () {
      console.log(this)
    }
  },
  computed: {
    modelNameToPascalCase: function () {
      return toPascalCase(this.modelName)
    }
  },
  emits: ['update:sortByField', 'update:pageSize'],
  setup (props) {
    return {}
  }
}
</script>
