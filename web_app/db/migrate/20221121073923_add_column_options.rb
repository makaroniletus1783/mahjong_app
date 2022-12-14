class AddColumnOptions < ActiveRecord::Migration[7.0]
  def up
    add_column :rises, :win_title, :string

    add_column :rises, :player_wind, :string
    add_column :rises, :round_wind, :string
    add_column :rises, :is_richi, :boolean, default: false, null: false
    add_column :rises, :is_tumo, :boolean, default: false, null: false
    add_column :rises, :is_rinshan, :boolean, default: false, null: false
    add_column :rises, :is_ippatu, :boolean, default: false, null: false
    add_column :rises, :is_chankan, :boolean, default: false, null: false
    add_column :rises, :is_haitei, :boolean, default: false, null: false
    add_column :rises, :is_houtei, :boolean, default: false, null: false
    add_column :rises, :is_daburu_riichi, :boolean, default: false, null: false
    add_column :rises, :is_nagashi_mangan, :boolean, default: false, null: false
    add_column :rises, :is_tenhou, :boolean, default: false, null: false
    add_column :rises, :is_renhou, :boolean, default: false, null: false
    add_column :rises, :is_chiihou, :boolean, default: false, null: false
  end
end
