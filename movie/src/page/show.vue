<template>
	<div class="mshow" >
		 <div class="content">
		 	<div class="main">
		 		<div class="box" v-for="item in showData">
		 			<img  v-if="item.poster_path" :src="basicImgSrc + item.poster_path">
		 			<div v-else  class="nopic"><img src="../assets/pic.png"></div>
		 			<div class="info">
		 				<p><strong>{{item.title}}</strong></p>
		 				<p>
		 					<span v-if="item.vote_count!=0">{{item.vote_average}}</span>
		 					<span v-else>no ratings</span>
		 					<span v-if="item.release_date">{{item.release_date}}</span>
		 					<span v-else>no release date</span>
		 				</p>
		 				<p></p>
		 				<p v-if="item.overview">{{overviewChange(item.overview)}}</p>
		 				<p v-else>No overview Data</p>
		 				<div class="more" @click="getDetail(item.id)">
		 					More
		 				</div>
		 			</div>
		 		</div>
		 	</div>
		 	<div class="page">
		 		<div class="mes">
		 			<p>current page:{{page}} of {{total_page}}</p>
		 			<p>results:{{total_result}}</p>
		 		</div>
		 		<div class="change">
		 			<img src="../assets/leftcircle.png" v-if="page > 1" @click="changePage(0)">
		 			<img src="../assets/rightcircle.png" v-if = "page < total_page"  @click="changePage(1)">
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
		watch:{
			$route(){
				if(this.$route.path.indexOf('search') != -1)
				{
					this.movieType = 'search';
					this.searchData = this.$route.query.val;
				}
				else if(this.$route.path.indexOf('top') != -1)
					this.movieType = 'top_rated';
				else
					this.movieType = 'popular';
				this.showData = [];
				this.page = 1;
				this.getMovie();
			}
		},
		data(){
			return{
				showData:null,
				total_page:null,
				page:1,
				total_result:null,
				basicImgSrc:'https://image.tmdb.org/t/p/w185',
				movieType:null,
				searchData:null
			}
		},
		mounted(){
			if(this.$route.path.indexOf('search') != -1)
			{
				this.movieType = 'search';
				this.searchData = this.$route.query.val;
			}
			else if(this.$route.path.indexOf('top') != -1)
				this.movieType = 'top_rated'
			else
				this.movieType = 'popular'

			this.getMovie();
		},
		methods:{
			overviewChange(word){
				return word.slice(0,180)+ '...'
			},
			changePage(type){
				if(type == 1)
					this.page ++;
				else
					this.page --;

				this.getMovie();
			},
			getMovie(){
				this.showData = [];
				if(this.movieType == 'search')
					this.axios.get('https://api.themoviedb.org/3/search/movie?api_key=6e13583a127e758dac0d94b26b7068bf&language=en-US&query='+this.searchData+'&page='+this.page+'&include_adult=false').
					then((res)=>{
						this.page = res.data.page;
						this.total_page =res.data.total_pages;
						this.total_result = res.data.total_results;
						this.showData = (res.data.results);
						console.log(res.data);
						document.documentElement.scrollTop = 0;
						document.body.scrollTop = 0;
					}).catch((err)=>{
						console.log(err);
					})
					
				else
					this.axios.get('https://api.themoviedb.org/3/movie/'+this.movieType+'?api_key=6e13583a127e758dac0d94b26b7068bf&language=en-US&page='+this.page).
					then((res)=>{
						this.page = res.data.page;
						this.total_page =res.data.total_pages;
						this.total_result = res.data.total_results;
						this.showData = (res.data.results);
						document.documentElement.scrollTop = 0;
						document.body.scrollTop = 0;
					}).catch((err)=>{
						console.log(err);
					})
			},
			getDetail(id){
				this.$router.push({path:'/movie/'+id})
			}
		}
	}
</script>
<style type="text/css" lang="less" scoped>
	.mshow{
		padding-top: 60px;
		width: 100%;
		.content{
			width: 100%;
			background-color:#f4f4f4;
			display: flex;
			flex-direction: column;
			align-items: center;

			.main{
				width:1000px;
				padding:0 20px;
				display: flex;
				flex-wrap: wrap;
				justify-content: space-between;
				.box{
					margin-top:40px;
					display: flex;
					height:278px;
					box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
					img{
						width:185px;
					}
					.info{
						width:298px;
						box-sizing: border-box;
						padding:10px 16px 16px 16px;
						position: relative;
						p{
							margin:0;
						}
						p:first-child{
							font-size: 18px;
							margin-bottom: 10px;
						}
						p:nth-child(2){
							color:rgba(0,0,0,0.6);
							margin-bottom: 5px;
						}
						.more{
							position: absolute;
							bottom:0;
							height:50px;
							padding:0 20px;
							line-height: 50px;
							width:100%;
							box-sizing: border-box;
							cursor: pointer;
							border-top:1px solid #d6d6d6;
							left:0;
						}
					}
					.nopic{
						width:185px;
						height:278px;
						background-color:#dbdbdb;
						display: flex;
						justify-content: center;
						align-items: center;
						img{
							width:64px;
						}
					}
				}
			}
			.page{
				width: 1000px;
				padding:30px 20px;
				display: flex;
				justify-content: space-between;
				align-items: center;
				.mes{
					p{
						margin:5px;
					}
					p:nth-child(2){
						color:rgba(0,0,0,0.5);
					}
				}
				.change{
					img{
						cursor: pointer;
						width:32px;
					}
					img + img{
						margin-left: 5px;

					}
				}
			}
		}
	}
</style>