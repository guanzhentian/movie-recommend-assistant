import Vue from 'vue'
import Router from 'vue-router'
import index from '@/page/index'
import recommend from '@/page/recommend'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: index
    },
    {
    	path:'/recommend',
    	component:recommend
    }
  ]
})
