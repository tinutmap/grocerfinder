<template >
  <form class="form-group">
    <p
      v-for="i in okMessages"
      :key="i.key"
      :value="i.value"
      class="alert alert-success"
    >
      {{ i }}
    </p>
    <ul v-if="nonFieldErrors.length > 0" class="alert alert-warning">
      <li v-for="i in nonFieldErrors" :key="i.key" :value="i.value">
        {{ i }}
      </li>
    </ul>
    <ul v-if="hiddenErrors.length > 0" class="alert alert-warning">
      <li v-for="i in hiddenErrors" :key="i.key" :value="i.value">
        {{ i }}
      </li>
    </ul>
    <div v-for="key in Object.keys(formData)" :key="key">
      <label :for="'field-' + key" class="control-label">{{
        camelCaseToPascalCase(key)
      }}</label>
      <span :id="'field-errors-' + key" class="error-field text-danger">
        {{ fieldErrors[key] }}
      </span>
      <br />
      <input
        v-if="formElement[key] === 'input-text'"
        type="text"
        required
        :id="'field-' + key"
        :value="formData[key]"
        @input="$emit('update:formData', key, $event.target.value)"
        class="form-control"
        v-bind:class="{ 'is-invalid': fieldErrors[key] }"
      />
      <input
        v-else-if="formElement[key] === 'input-number'"
        type="number"
        required
        :id="'field-' + key"
        :value="formData[key]"
        @input="$emit('update:formData', key, parseFloat($event.target.value))"
        class="form-control"
        v-bind:class="{ 'is-invalid': fieldErrors[key] }"
      />
      <div
        v-else-if="formElement[key] === 'select-option'"
        class=" input-group"
      >
        <select
          :value="formData[key].id"
          @input="$emit('update:formData', key + '.id', $event.target.value)"
          :id="'field-' + key"
          class="form-control"
          required
        >
          <option disabled v-if="isNew" value="">--Select {{ key }}--</option>
          <option
            v-for="i in selectOptionData[key]"
            v-bind:key="i.id"
            v-bind:value="i.id"
            v-bind:selected="i.id === formData[key].id"
            v-bind:class="{ 'is-invalid': fieldErrors[key] }"
          >
            {{ i.name }}
          </option>
        </select>
        <create-button @click="createNewKeyData(key)" />
        <update-button @click="updateKeyDataById(key, formData[key].id)" />
        <list-view-button @click="listViewKey(key)" />
        <delete-button @click="listViewKey(key)" />
      </div>
    </div>
    <input
      type="button"
      v-if="isNew"
      value="Create"
      @click="$emit('create')"
      class="btn btn-primary"
    />
    <input
      type="button"
      v-else
      value="Update"
      @click="$emit('update')"
      class="btn btn-primary"
    />
  </form>
</template>
<script>
import { camelCaseToPascalCase } from './Base.js'
import CreateButton from './button/CreateButton.vue'
import ListViewButton from './button/ListViewButton.vue'
import UpdateButton from './button/UpdateButton.vue'
import DeleteButton from './button/DeleteButton.vue'

export default {
  name: 'ModelDetailFormView',
  data: function () {
    return {}
  },
  props: {
    modelName: {
      type: String,
      required: true
    },
    formData: {
      type: Object
    },
    isNew: {
      type: Boolean,
      required: true,
      default: true
    },
    selectOptionData: {
      type: Object
    },
    formElement: {
      type: Object,
      required: true
    },
    nonFieldErrors: {
      type: Array
    },
    fieldErrors: {
      type: Object
    },
    hiddenErrors: {
      type: Array
    },
    okMessages: {
      type: Array
    },
    modelValue: {
      type: Object
    }
  },
  emits: ['update:formData', 'update', 'create', 'deleteKeyDataById'],
  methods: {
    camelCaseToPascalCase,
    createNewKeyData (key) {
      // this.$router.push('/' + key + '/create')
      window.open('/' + key + '/create', '', 'fullscreen=false')
    },
    listViewKey (key) {
      window.open('/' + key, '', 'fullscreen=false')
    },
    updateKeyDataById (key, id) {
      window.open('/' + key + '/' + id, '', 'fullscreen=false')
    }
  },
  components: { CreateButton, ListViewButton, UpdateButton, DeleteButton }
}
</script>
