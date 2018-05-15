<template>
	<div class="mv-header" >
		<div class="content">
			<div class="box1">
				<router-link tag="h1" to="/">LOGO</router-link>
				<router-link tag="span" to="/recommend/self">Recommendation</router-link>
				<router-link tag="span" to="/recommend/popular">Popular</router-link>
				<router-link tag="span" to="/recommend/top">Top Rated</router-link>	
			</div>
			<div class="box2">
				<div class="input">
					<input type="text" class="search" placeholder="Search" @keyup.enter = "search" v-model="searchData">
					<img src="../assets/search.png" @click="search" >
				</div>
				<router-link tag='div' to="/user" class="self" v-if="isLogin">
					{{name.slice(0,1).toUpperCase()}}
				</router-link>
				<div class="self2" v-else>
					<router-link tag="span" to="/register">Sign In</router-link>
					<router-link tag="span" to="/login">Login</router-link>
				</div>
			</div>
			<div class="box3">
				<div class="fb">
					<router-link tag="h1" to="/">LOGO</router-link>	
				</div>
				<div class="input"  v-show="isShow">
					<input type="text" class="search" placeholder="Search" @keyup.enter = "search" v-model="searchData">
					<img src="../assets/search.png" @click="search" >
				</div>
				<div class="sb">
					<div class="more" @click="isShow = !isShow">
						=
					</div>
				</div>
			</div>
			<div class="box4" v-show="isShow">
				<router-link tag="div" class="item" to="/recommend/self">Recommendation</router-link>
				<router-link tag="div" class="item" to="/recommend/popular">Popular</router-link>
				<router-link tag="div" class="item" to="/recommend/top">Top Rated</router-link>	
				<router-link tag='div' to="/user" class="self item" v-if="isLogin">User</router-link>
				<div class="self2" v-else>
					<router-link tag="div" class="item" to="/register">Sign In</router-link>
					<router-link tag="div" class="item" to="/login">Login</router-link>
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

			this.checkLogin();
			this.isShow = false;
		}
	},
	data(){
		return{
			searchData:'',
			isLogin:false,
			name:'',
			isShow:false
		}
		
	},
	mounted(){
		// grab an element
		var myElement = document.querySelector("div.mv-header");
		// construct an instance of Headroom, passing the element
		var headroom  = new Headroom(myElement);
		// initialise
		headroom.init();

		this.checkLogin();
	},
	methods:{
		search(){
			if(this.searchData == '')
				return
			this.$router.push({path:'/recommend/search?val='+this.searchData});
		},
		checkLogin(){
			this.axios.get('checkLogin')
			.then((res)=>{
				if(res.data.status)
				{
					this.isLogin = true;
					this.name = res.data.name;
				}
			})
			.catch((err)=>{
				console.log(err);
			});
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
			position: relative;
			padding:0 20px;
			width:1200px;
			display: flex;
			align-items: center;
			justify-content: space-between;
			color:rgba(255,255,255,0.85);
			.box1{
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
			.box2{
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
			.box3,.box4{
				display: none;
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

	@media screen and(max-width: 1024px) {
		.mv-header{
			height:40px;
			.content{
				.box1,.box2{
					display: none;
				}
				.box3{
					height:40px;
					width:100%;
					display: flex;
					align-items: center;
					justify-content: space-between;
					.fb{
						h1{
							margin:0;
							line-height: 40px;
							font-size:28px;
						}	
					}
					.sb{
						.more{
							height:25px;
							line-height: 25px;
							padding:0 10px;
							background-color:rgba(255, 255, 255, 0.9);
							border-radius: 3px;
							color:#081c24;
						}
					}
					.input{
						position: relative;
						margin-left: 10px;
						flex:0 1 200px;
						input{
							width:90%;
						}
						img{
							position: absolute;
							left:5px;
							top:6px;
							width: 20px;
							cursor: pointer;
						}
						.search{
							background-color:lighten(#24292e,10%) ;
							color:white;
							height:30px;
							border:0;
							padding-left:30px;
							box-sizing: border-box;
						}
					}
					input.search:focus{
						outline:0;
						background-color: lighten(#24292e,15%) 
					}
				}
				.box4{
					width:100%;
					position: absolute;
					top:40px;
					left:0;
					display: block;
					background-color:lighten(#081c24,5%);
					.item{
						height:40px;
						line-height: 40px;
						text-indent: 30px;
						border-bottom:1px solid rgba(255, 255, 255, 0.5);
					}
					
				}
			}
		}
	}
</style>