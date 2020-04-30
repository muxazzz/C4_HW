<template>
  <div class="alert">
    <b-alert v-show="isHidden"
      variant="danger"
      dismissible
      fade
      v-model="showDismissibleAlert"
    >{{ message }}</b-alert>
    <div v-if="!isHidden" class="alert alert-warning" id="alert" role="alert">
  {{ message }}
</div>
<button v-on:click="isHidden = !isHidden">Показать/скрыть уведомление</button>
</div>
</template>

<style>
</style>

<script>
export default {
  props: ['message', 'showDismissibleAlert=false'],
  data() {
    return {
      showDismissibleAlert: false,
      isHidden: false,
    };
  },
};
</script>
