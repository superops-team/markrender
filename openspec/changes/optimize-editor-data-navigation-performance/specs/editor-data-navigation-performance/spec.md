# editor-data-navigation-performance Specification

## ADDED Requirements

### Requirement: Content saves SHALL preserve item metadata

The system SHALL provide a content-save path for editor-originated content changes. This path SHALL update only `content`, `content_md5`, and `updated_at`, plus explicitly required page identity fields if provided. It SHALL NOT update import metadata, tags, tree fields, icon fields, display fields, or conversion status.

#### Scenario: Saving edited content preserves import metadata

- **GIVEN** an existing item has non-empty `file_path`, `converter`, and `status`
- **WHEN** the editor saves changed Markdown or Excalidraw content through the content-save path
- **THEN** `content`, `content_md5`, and `updated_at` are updated
- **AND** `file_path`, `converter`, and `status` keep their previous values

#### Scenario: Saving edited content preserves organization metadata

- **GIVEN** an existing item has `tags`, `parent_id`, `order`, `level`, `is_folder`, `icon_type`, `icon_path`, `icon_color`, and `display_name`
- **WHEN** the editor saves changed content through the content-save path
- **THEN** those metadata fields keep their previous values

#### Scenario: Explicit metadata update can clear metadata

- **GIVEN** an existing item has non-empty `tags`
- **WHEN** a metadata update operation explicitly passes `tags=""`
- **THEN** `tags` is cleared
- **AND** this behavior is not triggered by editor content save

### Requirement: Existing `save_item` behavior SHALL remain compatible for creation flows

The system SHALL keep existing item creation behavior compatible while changing existing-record updates to patch semantics.

#### Scenario: Creating an item without optional metadata

- **GIVEN** caller creates a new item without optional metadata fields
- **WHEN** the create path runs
- **THEN** existing defaults such as processed status and markdown page type are preserved

#### Scenario: Updating an existing item with omitted optional field

- **GIVEN** an existing item has `status="processed"`
- **WHEN** an update omits `status`
- **THEN** `status` remains `processed`

### Requirement: Failed frontend reads SHALL NOT be persisted as empty content

The system SHALL distinguish frontend read failure from intentional empty content. If the frontend editor is not ready or no editor instance exists, the system SHALL NOT save empty content.

#### Scenario: Markdown editor is not ready

- **GIVEN** the Markdown WebView exists but `window.editorState.editor` is missing
- **WHEN** backend requests `getContent`
- **THEN** the JS handler returns `success:false`
- **AND** the response includes `ready:false`
- **AND** the response includes `error_code:"EDITOR_NOT_READY"`
- **AND** backend does not update the DB content

#### Scenario: Excalidraw editor is not ready

- **GIVEN** the Excalidraw WebView exists but no supported content API is ready
- **WHEN** backend requests `getContent`
- **THEN** the JS handler returns `success:false`
- **AND** the response includes `ready:false`
- **AND** the response includes `error_code:"EDITOR_NOT_READY"`
- **AND** backend does not update the DB content

#### Scenario: User intentionally clears content

- **GIVEN** the editor is ready
- **AND** the frontend response has `success:true` and `ready:true`
- **AND** the response content is empty
- **WHEN** the backend saves the content
- **THEN** the DB content is updated to empty content

### Requirement: Programmatic content loading SHALL NOT mark content dirty

The system SHALL separate programmatic content loading from user editing. Loading DB content into the editor SHALL NOT mark the item dirty, schedule autosave, or create history.

#### Scenario: Loading item detail from DB

- **GIVEN** the user selects a document
- **WHEN** DB content is loaded into the editor
- **THEN** the editor displays the content
- **AND** `content_changed` remains false
- **AND** the autosave timer is not started by this load
- **AND** no history record is created solely because of this load

#### Scenario: User edits after load

- **GIVEN** DB content has finished loading
- **WHEN** the user changes editor content
- **THEN** the editor marks the item dirty
- **AND** autosave or deferred save scheduling may occur

### Requirement: Page navigation SHALL apply frontend state once for the active navigation token

The system SHALL ensure that one logical document switch applies target content only for the active navigation token. Stale delayed callbacks SHALL NOT overwrite the current document.

#### Scenario: Same page type document switch

- **GIVEN** the current document and target document both use `page_type="markdown"`
- **WHEN** the user switches documents
- **THEN** the system does not reset frontend state solely because the item changed
- **AND** the active navigation token calls `setValue` at most once

#### Scenario: Different page type document switch

- **GIVEN** the current document uses Markdown and the target document uses Excalidraw
- **WHEN** the user switches documents
- **THEN** the system switches page type
- **AND** reset occurs only as part of the page-type transition
- **AND** the target content is applied once after the target page is ready

#### Scenario: Stale delayed callback fires

- **GIVEN** navigation token A is superseded by navigation token B
- **WHEN** a delayed callback from token A tries to call `setValue`
- **THEN** the callback is ignored
- **AND** token B content remains visible

### Requirement: Regular navigation SHALL avoid long synchronous save waits

The system SHALL avoid using the 15s synchronous JS read path as the normal document-switch gate. Navigation MAY schedule a pending save, but it SHALL NOT block the target document load on a long `send_message_sync('getContent')` wait during regular switching.

#### Scenario: Switching with captured dirty content

- **GIVEN** the current document has dirty content already captured in backend memory
- **WHEN** the user selects another document in QuickPick
- **THEN** the dirty content is scheduled for save
- **AND** the target document begins loading without waiting for a 15s synchronous JS timeout

#### Scenario: Switching when frontend content cannot be read

- **GIVEN** the current document is dirty but frontend `getContent` returns `EDITOR_NOT_READY`
- **WHEN** the user selects another document
- **THEN** the system does not save empty content
- **AND** the item remains dirty or reports a visible save warning
- **AND** navigation may continue without overwriting DB content

#### Scenario: Closing the application flushes pending saves

- **GIVEN** there are pending save operations
- **WHEN** the user closes the application
- **THEN** the system attempts to flush pending saves with a bounded timeout
- **AND** if flushing fails, the user receives a visible warning
- **AND** failed reads are not saved as empty content

### Requirement: QuickPick tree loading SHALL use lightweight node data

The system SHALL load tree data without fetching document body content. Full document content SHALL be loaded only when a document detail is explicitly requested.

#### Scenario: Loading the full tree

- **GIVEN** the database contains documents and folders
- **WHEN** QuickPick loads the tree
- **THEN** each node includes identity, title, tags, page type, tree fields, icon fields, and timestamps
- **AND** each node excludes `content`
- **AND** tree construction does not issue one database query per node

#### Scenario: Opening a document from the tree

- **GIVEN** a QuickPick tree node excludes `content`
- **WHEN** the user opens that document
- **THEN** the system loads full content through the existing detail-read path

#### Scenario: Filtering tree by search text

- **GIVEN** the user types in the QuickPick search box
- **WHEN** the search text changes rapidly
- **THEN** filtering is debounced
- **AND** drag/drop setup is not repeatedly installed during a single filter operation

### Requirement: Disk sync failures SHALL be observable

The system SHALL not treat local output write failure as silent success.

#### Scenario: Disk sync fails after DB save

- **GIVEN** DB content save succeeds
- **WHEN** local output file writing fails
- **THEN** the write function returns a failure result or raises a handled error
- **AND** the application records a visible unsynced/save-warning state
- **AND** the exception is not only swallowed as a log line

#### Scenario: User clears a document

- **GIVEN** an item previously had non-empty content and a local output file
- **WHEN** the user intentionally saves empty content
- **THEN** the DB content becomes empty
- **AND** the local output file is updated to empty content
- **AND** stale old output content is not left behind as the current disk representation

### Requirement: Autosave SHALL coalesce high-frequency edits without recording programmatic loads

The system SHALL debounce autosave for user edits and SHALL NOT create history entries for programmatic content loads.

#### Scenario: Frequent user edits

- **GIVEN** a user changes a document repeatedly within the debounce window
- **WHEN** autosave runs
- **THEN** only the latest captured user content is saved for that debounce cycle

#### Scenario: Programmatic load happens during navigation

- **GIVEN** a document is loaded from DB during navigation
- **WHEN** content is applied to the editor
- **THEN** autosave is not scheduled for that programmatic load

### Requirement: Test harness SHALL fail on missing tests or import errors

The project test runner SHALL fail when requested tests cannot be imported or when no tests are executed.

#### Scenario: Listed test module cannot be imported

- **GIVEN** `test/run_all_tests.py` lists or discovers a test module
- **WHEN** the module import fails
- **THEN** the runner exits non-zero
- **AND** the failed module name is printed

#### Scenario: No tests are discovered

- **GIVEN** the test runner executes zero tests
- **WHEN** the run completes
- **THEN** the runner exits non-zero
- **AND** the output states that no tests were run

#### Scenario: Regression tests protect persistence and navigation

- **GIVEN** this optimization change is implemented
- **WHEN** targeted tests run
- **THEN** tests cover metadata preservation, editor-not-ready behavior, intentional empty content, programmatic load dirty state, single setValue navigation, stale token ignoring, lightweight tree loading, and disk sync failure reporting
