<template>
  <div v-if="!loading">
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
    <select name="" id="pageSize" v-model="pageSize">
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
    <select name="" id="sortByField" :value="sortByField" v-model="sortByField">
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
    <button @click="doFetchMore" class="btn btn-primary">
      Load More
    </button>
  </div>
</template>

<script>
import RawDataTable from './RawDataTable.vue'
import { toPascalCase } from './Base.js'
import { ref, computed, watch } from 'vue'
export default {
  name: 'ModelListView',
  data () {
    return {
      checkedBox: [],
      okMessage: [],
      errorMessage: []
    }
  },
  components: {
    RawDataTable
  },
  props: {
    modelName: {
      type: String,
      required: true
    },
    deleteMutation: {},
    sortedFields: {
      type: Array,
      required: true
    },
    doModelFetchMore: {
      type: Function,
      require: true
    }
  },
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
          this.okMessage = []
          data = data.data['delete' + this.modelNameToPascalCase]

          // Removed id deleted in idNotExist array from this.modelData array
          this.modelData = this.modelData.filter(
            element => !data.idNotExist.includes(element.id)
          )

          // Removed id deleted in idDeleted array from this.modelData array
          this.modelData = this.modelData.filter(
            element => !data.idDeleted.includes(element.id)
          )

          // Removed id not exist in idNotExist array from this.checkedBox array
          this.checkedBox = this.checkedBox.filter(
            id => !data.idNotExist.includes(id)
          )

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
    }
  },
  computed: {
    modelNameToPascalCase: function () {
      return toPascalCase(this.modelName)
    }
  },
  setup (props) {
    const sortByField = ref(props.sortedFields[0])
    const pageSizeOptions = [5, 10, 25, 50, 100]
    const pageSize = ref(pageSizeOptions[0])
    const cursorInitial = 0
    const cursorIdInitial = 0
    const modelData = ref([])
    const { data, loading, refetch, onResult } = props.doModelFetchMore(
      cursorInitial,
      cursorIdInitial,
      pageSize.value,
      sortByField.value
    )
    onResult(_ => {
      if (data.value.length > 0) {
        modelData.value.length > 0
          ? modelData.value.push(...data.value)
          : (modelData.value = data.value)
      }
    })
    const cursor = computed(() => {
      return modelData.value[modelData.value.length - 1][sortByField.value]
    })
    const cursorId = computed(() => {
      return modelData.value[modelData.value.length - 1].id
    })
    function doFetchMore () {
      refetch({
        cursor: String(cursor.value),
        cursor_id: cursorId.value,
        page_size: pageSize.value,
        sort_by_field: sortByField.value
      })
    }
    watch([pageSize, sortByField], newValue => {
      refetch({
        cursor: String(cursorInitial),
        cursor_id: cursorIdInitial,
        page_size: newValue[0],
        sort_by_field: newValue[1]
      })
    })
    return {
      sortByField,
      pageSizeOptions,
      pageSize,
      modelData,
      loading,
      doFetchMore
    }
  }
}
</script>
