class MahjongsController < ApplicationController
  require "net/http"
  require "uri"
  require "json"

  @@minkan = []
  @@annkan = []
  @@chi = []
  @@pon = []
  @@chankan = []
  @@nuki_dora = []
  @@dora = []
  @@ura_dora = []

  def new
    @rise = Rise.new
  end

  def create
    #binding.pry
    @rise = Rise.new(rise_params)
    @@minkan = check(params[:minkan])
    @@annkan = check(params[:annkan])
    @@chi = check(params[:chi])
    @@pon = check(params[:pon])
    @@chankan = check(params[:chankan])
    @@nuki_dora = check(params[:nuki_dora])
    @@dora = check(params[:dora])
    @@ura_dora = check(params[:ura_dora])

    if @rise.save
      redirect_to result_path(@rise)
    else
      render :new, status: :unprocessable_entity
    end
  end

  def result
    @rise = Rise.find(params[:id])
    begin
      image_url = @rise.image_url
      win_tile = @rise.win_title

      uri = URI.parse("http://127.0.0.1:8000/mahjong/predict")
      request = Net::HTTP::Post.new(uri)
      request.content_type = "application/json"
      request["Accept"] = "application/json"
      request.body = JSON.dump({
        "image_url" => image_url,
        "minkan" => @@minkan,
        "annkan" => @@annkan,
        "chi" => @@chi,
        "pon" => @@pon,
        "chankan" => @@chankan,
        "nukidora" => @@nuki_dora,
        "dora" => @@dora,
        "ura_dora" => @@ura_dora,
        "win_tile" => @rise.win_title,
        "is_tsumo" => @rise.is_tumo,
        "is_riichi" => @rise.is_richi,
        "is_ippatsu" => @rise.is_ippatu,
        "is_rinshan" => @rise.is_rinshan,
        "is_chankan" => @rise.is_chankan,
        "is_haitei" => @rise.is_haitei,
        "is_houtei" => @rise.is_houtei,
        "is_daburu_riichi" => @rise.is_daburu_riichi,
        "is_nagashi_mangan" => @rise.is_nagashi_mangan,
        "is_tenhou" => @rise.is_tenhou,
        "is_renhou" => @rise.is_renhou,
        "is_chiihou" => @rise.is_chiihou,
        "player_wind" => @rise.player_wind,
        "round_wind" => @rise.round_wind,
      })

      req_options = {
        use_ssl: uri.scheme == "https",
      }

      response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
        http.request(request)
      end
      @response_body = JSON.parse(response.body)
    rescue Exception => e
      @error = e.message
      @parent = 0
      @child = 0
      @han = 0
      @fu = 0
      @yaku = nil
    else
      @parent = @response_body["parent"]
      @child = @response_body["child"]
      @fu = @response_body["fu"]
      @han = @response_body["han"]
      @yaku = @response_body["yaku"]
    end
  end

  private

  def rise_params
    params.require(:rise).permit(:image, :win_title, :player_wind, :round_wind, :is_chankan, :is_chiihou, :is_daburu_riichi, :is_haitei, :is_houtei, :is_ippatu, :is_nagashi_mangan, :is_renhou, :is_richi, :is_rinshan, :is_tenhou, :is_tumo)
  end

  def check(a)
    if a.present?
      return a
    else
      return []
    end
  end
end
