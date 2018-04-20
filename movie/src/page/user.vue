<template>
	<div class="muser">
		<div class="top" :style="{backgroundImage:'url('+bg+')'}">
			<div class="mengban">
				<div class="content" >
					<div class="name">
						官
					</div>
					<div class="info">
						<div class="small">
							<h1 >官少</h1><p>2018 April Join as a member of this website.</p>
						</div>
						
						<p>Average Movie Rating</p>
					</div>
				</div>	
			</div>
			
		</div>
		<div class="link">
			<div class="content">
				<span class="active">OVERVIEW</span>
			</div>
		</div>
		<div class="detail">
			<div class="content">
				<div class="box box1">
					<h2>STATUS</h2>
					<div class="status">
						<div>
							<p>评分总数</p>
							<div>
								0
							</div>
						</div>
						<div>
							<p>评分总览</p>
							<div>
								<span>1及以下：0</span>
								<span>2到1：0</span>
								<span>3到2：0</span>
								<span>4到3：0</span>
								<span>5到4：0</span>
							</div>
						</div>
					</div>
				</div>
				<div class="box box2">
					<h2>最近评论</h2>
					<div>
						你最近未评论
					</div>
				</div>
				<div class="box box2">
					<h2>最近浏览电影</h2>
					<div>
						你最近未浏览
					</div>
				</div>
			</div>
		</div>
		<foot></foot>
	</div>
</template>
<script type="text/javascript">
	import foot from '@/components/foot'
	export default{
		components:{
			foot
		},
		data(){
			return{
				bg:require('../assets/3.jpg')
			}
		}
	}
</script>
<style type="text/css" lang="less" scoped>
	.muser{
		padding-top: 60px;
		width: 100%;

		.top{	
			width:100%;
			background-position: center 10%;
			background-size: cover;
			background-repeat: no-repeat;
			.mengban{
				width:100%;
				display: flex;
				justify-content: center;
				background-color: rgba(0,0,0,0.5);
				.content{
					width:1000px;
					padding:40px 20px;
					display: flex;
					align-items: center;
					color:rgba(255,255,255,0.95);
					.name{
						width:150px;
						height:150px;
						border-radius: 50%;
						background-color:#d29001;
						color:white;
						font-size:64px;
						text-align: center;
						line-height: 145px;
						margin-right: 40px;
					}
					.info{
						.small{
							display: flex;
							align-items: flex-end;
							h1{
								margin:0;
								margin-right: 10px;
								font-size: 35.2px;
								font-weight: bold;
							}
							p{
								margin:0;
								font-size: 17.6px;
								color:#f4f4f4;
							}
						}
					}
				}	
			}
			
		}
		.link{
			width:100%;
			height:66px;
			background-color: white;
			border-bottom: 1px solid rgba(0, 0, 0, 0.1);
			display: flex;
			justify-content: center;
			.content{
				height:100%;
				width: 1000px;
				padding:0 20px;
				font-size: 20px;
				font-weight: bold;
				display: flex;
				span{
					display: flex;
					align-items: center;
				}
				.active{
					border-bottom: 5px solid #d29001;
				}
			}
		}
		.detail{
			width:100%;
			background-color: #f4f4f4;
			padding:30px 0px;
			display: flex;
			justify-content: center;
			border-bottom: 1px solid rgba(0, 0, 0, 0.1);
			.content{
				width:1000px;
				padding:0 20px;
			}
		}
	}
</style>