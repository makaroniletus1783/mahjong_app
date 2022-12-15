class MahjongsController < ApplicationController
  require "net/http"
  require "uri"
  require "json"

  def initialize()
    @win_tile = nil   #アガリ牌
    @melds = false   #鳴き
    @dora = nil  #ドラ
    @dora_ura = nil  #裏ドラ
    @player_wind = nil  #自風
    @round_wind = nil  #場風
    @is_richi = false  #リーチかどうか
    @is_tumo = false  #ツモかどうか
    @is_ippatu = false  #一発かどうか
    @is_rinshan = false  #嶺上開花かどうか
  end
  
  def new
  end

  def create
    #binding.pry
    @rise = Rise.new(rise_params)
    #@is_richi = true_or_false(params[:rise][:鳴き])
    if @rise.save
      redirect_to result_path(@rise)
    else
      render :new
    end
  end

  def result
    @rise = Rise.find(params[:id])
    begin
      image_url = @rise.image_url
      @is_richi = @rise.is_richi

      uri = URI.parse("http://127.0.0.1:8000/mahjong/predict")
      request = Net::HTTP::Post.new(uri)
      request.content_type = "application/json"
      request["Accept"] = "application/json"
      request.body = JSON.dump({
        "image_url" => image_url,
        "is_richi" => @is_richi
      })

      req_options = {
        use_ssl: uri.scheme == "https",
      }

      response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
        http.request(request)
      end
    rescue Exception => e
      @response_body = e.message
    else
      @response_body = JSON.parse(response.body)
    end
  end

  private

  def rise_params
    params.require(:rise).permit(:image, :is_richi, :is_ippatu, :is_rinshan, :is_tumo, :melds, :win_title, :dora, :dora_ura, :player_wind, :round_wind)

  end
end
