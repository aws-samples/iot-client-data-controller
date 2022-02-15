// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import Vue from 'vue'
import Router from 'vue-router'
import Home from './components/Home.vue'
import Vehicle from './components/Vehicle.vue'
import Add from './components/Add.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
      path: '/add',
      name: 'add',
      component: Add
  },
    {
      path: '/vehicle/:vin_number',
      name: 'vehicle',
      component: Vehicle
  },
  ]
})