<template>
	<div class="mindex">
		<myheader></myheader>
		<div class="box box1" :style="{backgroundImage:'url('+bg.bg2+')'}">
			<div class="content">
				<div class="main">
					<h1>Welcome To</h1>
					<h1>The Movie Recommendation System</h1>
					<div class="bot">
						<span>How To Use?</span>
						<img src="../assets/down.png" alt="">	
					</div>
					
				</div>
			</div>
		</div>
		<div class="box box2" >
			<div class="content">
				<h1><div class="one">1</div>First Step</h1>
				<p>You need to register and sign in</p>
				<div class="zcbtn">
					REGISTER NOW!
				</div>
				<p>Or you can click on Register in the upper right corner</p>
				<h1><div class="one">2</div>Second Step</h1>
				<p>You need to complete our recommended test</p>
				<p>Then we will give you a calculated recommendation</p>
				<p>Like this</p>
				<img src="../assets/m1.png" alt="">
			</div>
		</div>
		<div class="box box3"  :style="{backgroundImage:'url('+bg.bg4+')'}">
			<div class="content">
				<div class="main">
					<h1>How the Recommendation System work?</h1>
					<div class="content2">
						<p>We use a hybrid recommendation method, one based on film features and the other based on SVD.When you have completed the recommended test,SVD-based recommendations are not calculated immediately, because of the time overhead, it will only be calculated over a certain period of time.</p>
						<p>The recommendation based on film characteristics is the same as literal meaning. It is based on the features of the movie and is weighted. Finally, the movie closest to it is calculated and then recommended.</p>
						<p>The recommendation method based on the SVD algorithm is based on the rating history of all users and comprehensively calculates the movie you will like.</p>
						<p>In these recommended methods, some features unique to this site are added for weighted calculations.</p>	
					</div>
					
				</div>
				
			</div>
		</div>
		<foot></foot>
	</div>
</template>
<script type="text/javascript">
	import myheader from '@/components/header'
	import foot from '@/components/foot'
	export default{
		components:{
			myheader,foot
		},
		data(){
			return{
				bg:{

					bg2:require('../assets/5.jpg'),
					bg4:require('../assets/4.jpg'),
				}
			}
		}
	}	
</script>
<style type="text/css" lang="less" scoped>
	.mindex{
		padding-top: 60px;
	}
	.box{
		background-position: center;
		background-size: cover;
	}
	.box1{
		width: 100%;
		height:800px;
		.content{
			background-color: rgba(0,0,0,0.2);
			width: 100%;
			height:100%;
			display: flex;
			justify-content: center;
			.main{
				position: relative;
				width: 1200px;
				padding:0 20px;
				color:rgba(255,255,255,1);
				display: flex;
				flex-direction: column;
				justify-content: center;
				h1{
					position: relative;
					top:-80px;
					margin:0;
					font-size:50px;
					text-align: center;
				}
				.bot{
					width: 100%;
					position: absolute;
					bottom:30px;
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
					span{
						font-size: 20px;
					}
					img{
						margin-top: 20px;
						width: 30px;
					}
				}
				
			}
		}
	}
	.box2{
		width: 100%;
		height:800px;
		display: flex;
		justify-content: center;
		.content{
			width: 1200px;
			padding:0 20px;
			color:#081c24;
			text-align: center;
			display: flex;
			flex-direction: column;
			h1{
				display: flex;
				align-items: center;
				.one{
					margin-right: 30px;
					display: inline-block;
					font-size:20px;
					background-color: #081c24;
					color:white;
					width:30px;
					height:30px;
					border-radius: 50%;
					line-height: 30px;
					text-align: center;
				}
			}
			p{
				font-size: 20px;
			}
			.zcbtn{
				align-self: center;
				width:200px;
				height:80px;
				line-height: 80px;
				background-color: #081c24;
				color:rgba(255,255,255,0.85);
				cursor: pointer;
				border-radius: 10px;
				&:hover{
					background-color: lighten( #081c24,5%);
				}
				&:active{
					background-color: lighten( #081c24,10%);
				}
			}
			>img{
				align-self:center 
			}
		}
	}
	.box3{
		width: 100%;
		height:800px;
		.content{
			background-color: rgba(0,0,0,0.2);
			width: 100%;
			height:100%;
			display: flex;
			justify-content: center;
			.main{
				width:1200px;
				padding:0 20px;
				color:white;
				display: flex;
				flex-direction: column;
				h1{
					position: relative;
					left:100px;
				}
				.content2{
					align-self: center;
					width:800px;
					position: relative;
					top:80px;
					p{
						color:rgba(255,255,255,0.9);
						text-indent: 2em;
						font-size: 20px;
					}	
				}
				
			}
			
		}
	}
</style>