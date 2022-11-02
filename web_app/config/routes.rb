Rails.application.routes.draw do
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  # root "articles#index"

  get root to: "mahjongs#new"
  post "/mahjong" => "mahjongs#create"
  get "/mahjong/result/:id" => "mahjongs#result", as: "result"
end
