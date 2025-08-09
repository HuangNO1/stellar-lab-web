<template>
  <n-config-provider :locale="zhCN" :date-locale="dateZhCN">
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-message-provider>
            <n-layout style="min-height: 100vh;">
              <n-layout-header style="height: 64px; padding: 24px">
                <Header />
              </n-layout-header>
              <n-layout-content style="padding: 24px">
                <router-view />
              </n-layout-content>
              <n-layout-footer style="padding: 24px; text-align: center;">
                <Footer />
              </n-layout-footer>
            </n-layout>
            <n-global-style />
          </n-message-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { zhCN, dateZhCN } from 'naive-ui'
import Header from '@/components/layout/Header.vue'
import Footer from '@/components/layout/Footer.vue'
</script>