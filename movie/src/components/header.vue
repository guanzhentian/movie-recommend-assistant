<template>
	<div class="mv-header" >
		<div class="content">
			<div>
				<router-link tag="h1" to="/">LOGO</router-link>
				<router-link tag="span" to="/recommend/self">Recommendation</router-link>
				<router-link tag="span" to="/recommend/popular">Popular</router-link>
				<router-link tag="span" to="/recommend/top">Top Rated</router-link>	
			</div>
			<div>
				<div class="input">
					<input type="text" class="search" placeholder="Search" @keyup.enter = "search" v-model="searchData">
					<img src="../assets/search.png" @click="search" >
				</div>
				<router-link tag='div' to="/user" class="self">
					M
				</router-link>
				<div class="self2">
					<router-link tag="span" to="/register">Sign In</router-link>
					<router-link tag="span" to="/login">Login</router-link>
				</div>
			</div>
			
			
		</div>
	</div>
</template>
<script type="text/javascript">
import Headroom from 	'headroom.js'

export default {
	watch:{
		$route(newv,oldv){
			if(newv.path != oldv.path)
				this.searchData = ''
		}
	},
	data(){
		return{
			searchData:''	
		}
		
	},
	mounted(){
		// grab an element
		var myElement = document.querySelector("div.mv-header");
		// construct an instance of Headroom, passing the element
		var headroom  = new Headroom(myElement);
		// initialise
		headroom.init();
	},
	methods:{
		search(){
			if(this.searchData == '')
				return
			this.$router.push({path:'/recommend/search?val='+this.searchData});
		}
	}
}
</script>
<style type="text/css" scoped lang="less">
	.mv-header{
		z-index:100;
		width:100%;
		position: fixed;
		top:0;
		height:60px;
		display: flex;
		justify-content: center;
		background-color: #081c24;
		.content{
			padding:0 20px;
			width:1200px;
			display: flex;
			align-items: center;
			justify-content: space-between;
			color:rgba(255,255,255,0.85);
			>div:first-child{
				display: flex;
				align-items: center;
				h1{
					cursor: pointer;
					margin:0px;
				}
				span{
					padding-left: 30px;
					cursor: pointer;
					transition: all .2s;
					&:hover{
						color:#805be7;
						transform: translateY(3px);
					}
				}	
			}
			>div:last-child{
				display: flex;
				align-items: center;
				.input{
					position: relative;
					img{
						position: absolute;
						left:5px;
						top:6px;
						width: 20px;
						cursor: pointer;
					}
				}
				.search{
					background-color:lighten(#24292e,10%) ;
					color:white;
					height:30px;
					border:0;
					padding-left:30px
				}
				input.search:focus{
					outline:0;
					background-color: lighten(#24292e,15%) 
				}
				.self{
					margin-left: 30px;
					width:35px;
					height:35px;
					border-radius: 50%;
					background-color: #d29001;
					color:white;
					text-align: center;
					line-height: 35px;
					cursor: pointer;
					transition: all .2s;
					&:hover{
						color:#081c24;
						transform: translateY(3px);
					}
				}
				.self2{
					span{
						padding-left: 30px;
						cursor: pointer;
						transition: all .2s;
						&:hover{
							color:#805be7;
							transform: translateY(3px);
						}
					}	
				}
			}
			
		}
	}
	.mv-header.headroom--pinned{
		animation: fadeInDown both 0.4s;
	}
	.mv-header.headroom--unpinned{
		animation: fadeOutUp both  0.4s;
	}
	@keyframes fadeInDown {
	  from {
	    // opacity: 0;
	    transform: translate3d(0, -100%, 0);
	  }

	  to {
	    opacity: 1;
	    transform: translate3d(0, 0, 0);
	  }
	}
	@keyframes fadeOutUp {
	  from {
	    opacity: 1;
	  }

	  to {
	    // opacity: 0;
	    transform: translate3d(0, -100%, 0);
	  }
	}
</style>