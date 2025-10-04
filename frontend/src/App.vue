<template>
  <n-config-provider>
    <n-message-provider>
      <n-dialog-provider>
        <n-loading-bar-provider>
          <div id="app">
            <router-view />
          </div>
        </n-loading-bar-provider>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
// Import'lar otomatik olarak global naive-ui'dan gelecek
</script>

<style>
#app {
  min-height: 100vh;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}
</style>