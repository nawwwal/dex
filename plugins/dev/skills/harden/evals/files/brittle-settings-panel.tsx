import { debounce } from 'lodash';

export function SettingsPanel({ user, onSave, onNavigate }: any) {
  const saveLater = debounce(() => onSave(user), 300);

  return (
    <section
      style={{ width: 920, position: 'relative', overflow: 'hidden' }}
      className="settings settings--custom"
    >
      <div className="settings__header">
        <h4>Account</h4>
        <div className="settings__link" onClick={() => onNavigate('/billing')}>
          Billing
        </div>
      </div>

      <img src="/avatars/current-user.png" />

      <div
        className="settings__save"
        onClick={saveLater}
        style={{ position: 'absolute', right: 13, top: 37 }}
      >
        Save changes
      </div>

      <style>{`
        .settings .settings__save {
          color: #4b2cff !important;
        }
        .settings .settings__header div:first-child + div {
          cursor: pointer;
        }
      `}</style>
    </section>
  );
}
