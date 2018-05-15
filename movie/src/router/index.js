import Vue from 'vue'
import Router from 'vue-router'
import index from '@/page/index'
import recommend from '@/page/recommend'
import register from '@/page/register'
import show from '@/page/show'
import movie from '@/page/movie'
import user from '@/page/user'
import test from '@/page/test'
import management from '@/page/management'

Vue.use(Router)

export default new Router({
  // mode: 'history',
  routes: [
    {
      path: '/',
      component: index
    },
    {
    	path:'/recommend/self',
    component:recommend
    	},
      {
        path:'/recommend/popular',
        component:show
      },
      {
        path:'/recommend/top',
        component:show
      },
          {
      path:'/register',
      component:register
    },
    {
      path:'/login',
      component:register
    },
    {
      path:'/recommend/search',
      component:show
    },
    {
      path:'/movie/:id',
      component:movie
    },
    {
      path:'/user',
      component:user
    },
    {
      path:'/test',
      component:test
    },
    {
      path:'/mana',
      component:management
    },
    {
      path:'*',
      redirect:'/'
    }
  ]
})
