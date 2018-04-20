<template>
  <div id="app">
  	<myheader></myheader>
    <router-view/>
  </div>
</template>

<script>
import myheader from '@/components/header'
export default {
  name: 'App',
  components:{
	myheader
	},
	watch:{
		$route(newv,oldv){
			if(newv.path != oldv.path)
			{
				document.documentElement.scrollTop = 0;
				document.body.scrollTop = 0;
			}
		}
	},
}
</script>

<style>
#app {
  
}
</style>
