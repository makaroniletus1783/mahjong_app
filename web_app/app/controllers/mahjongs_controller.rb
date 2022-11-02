class MahjongsController < ApplicationController
  require "net/http"
  require "uri"
  require "json"

  def new
  end

  def create
    @rise = Rise.new(rise_params)
    if @rise.save
      redirect_to result_path(@rise)
    else
      render :new
    end
  end

  def result
    @rise = Rise.find(params[:id])
    image_url = @rise.image_url

    uri = URI.parse("http://127.0.0.1:8000/mahjong/predict")
    request = Net::HTTP::Post.new(uri)
    request.content_type = "application/json"
    request["Accept"] = "application/json"
    request.body = JSON.dump({
      "image_url" => image_url,
    })

    req_options = {
      use_ssl: uri.scheme == "https",
    }

    response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
      http.request(request)
    end

    @response_body = JSON.parse(response.body)
  end

  private

  def rise_params
    params.require(:rise).permit(:image)
  end
end
